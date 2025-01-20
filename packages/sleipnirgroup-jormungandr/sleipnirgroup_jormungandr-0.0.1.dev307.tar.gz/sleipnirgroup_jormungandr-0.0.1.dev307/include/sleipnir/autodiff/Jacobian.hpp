// Copyright (c) Sleipnir contributors

#pragma once

#include <utility>

#include <Eigen/SparseCore>

#include "sleipnir/autodiff/ExpressionGraph.hpp"
#include "sleipnir/autodiff/Profiler.hpp"
#include "sleipnir/autodiff/Variable.hpp"
#include "sleipnir/autodiff/VariableMatrix.hpp"
#include "sleipnir/util/SymbolExports.hpp"
#include "sleipnir/util/small_vector.hpp"

namespace sleipnir {

/**
 * This class calculates the Jacobian of a vector of variables with respect to a
 * vector of variables.
 *
 * The Jacobian is only recomputed if the variable expression is quadratic or
 * higher order.
 */
class SLEIPNIR_DLLEXPORT Jacobian {
 public:
  /**
   * Constructs a Jacobian object.
   *
   * @param variables Vector of variables of which to compute the Jacobian.
   * @param wrt Vector of variables with respect to which to compute the
   *   Jacobian.
   */
  Jacobian(const VariableMatrix& variables, const VariableMatrix& wrt) noexcept
      : m_variables{std::move(variables)}, m_wrt{std::move(wrt)} {
    m_profiler.StartSetup();

    for (int row = 0; row < m_wrt.Rows(); ++row) {
      m_wrt(row).expr->row = row;
    }

    for (auto& variable : m_variables) {
      m_graphs.emplace_back(variable);
    }

    for (int row = 0; row < m_variables.Rows(); ++row) {
      if (m_variables(row).Type() == ExpressionType::kLinear) {
        // If the row is linear, compute its gradient once here and cache its
        // triplets. Constant rows are ignored because their gradients have no
        // nonzero triplets.
        m_graphs[row].AppendAdjointTriplets([&](int col, double adjoint) {
          m_cachedTriplets.emplace_back(row, col, adjoint);
        });
      } else if (m_variables(row).Type() > ExpressionType::kLinear) {
        // If the row is quadratic or nonlinear, add it to the list of nonlinear
        // rows to be recomputed in Value().
        m_nonlinearRows.emplace_back(row);
      }
    }

    for (int row = 0; row < m_wrt.Rows(); ++row) {
      m_wrt(row).expr->row = -1;
    }

    if (m_nonlinearRows.empty()) {
      m_J.setFromTriplets(m_cachedTriplets.begin(), m_cachedTriplets.end());
    }

    m_profiler.StopSetup();
  }

  /**
   * Returns the Jacobian as a VariableMatrix.
   *
   * This is useful when constructing optimization problems with derivatives in
   * them.
   */
  VariableMatrix Get() const {
    VariableMatrix result{VariableMatrix::empty, m_variables.Rows(),
                          m_wrt.Rows()};

    for (int row = 0; row < m_variables.Rows(); ++row) {
      auto grad = m_graphs[row].GenerateGradientTree(m_wrt);
      for (int col = 0; col < m_wrt.Rows(); ++col) {
        if (grad(col).expr != nullptr) {
          result(row, col) = std::move(grad(col));
        } else {
          result(row, col) = Variable{0.0};
        }
      }
    }

    return result;
  }

  /**
   * Evaluates the Jacobian at wrt's value.
   */
  const Eigen::SparseMatrix<double>& Value() {
    m_profiler.StartSolve();

    if (m_nonlinearRows.empty()) {
      m_profiler.StopSolve();
      return m_J;
    }

    for (auto& graph : m_graphs) {
      graph.Update();
    }

    // Copy the cached triplets so triplets added for the nonlinear rows are
    // thrown away at the end of the function
    auto triplets = m_cachedTriplets;

    // Compute each nonlinear row of the Jacobian
    for (int row : m_nonlinearRows) {
      m_graphs[row].AppendAdjointTriplets([&](int col, double adjoint) {
        triplets.emplace_back(row, col, adjoint);
      });
    }

    if (triplets.size() > 0) {
      m_J.setFromTriplets(triplets.begin(), triplets.end());
    } else {
      // setFromTriplets() is a no-op on empty triplets, so explicitly zero out
      // the storage
      m_J.setZero();
    }

    m_profiler.StopSolve();

    return m_J;
  }

  /**
   * Returns the profiler.
   */
  Profiler& GetProfiler() { return m_profiler; }

 private:
  VariableMatrix m_variables;
  VariableMatrix m_wrt;

  small_vector<detail::ExpressionGraph> m_graphs;

  Eigen::SparseMatrix<double> m_J{m_variables.Rows(), m_wrt.Rows()};

  // Cached triplets for gradients of linear rows
  small_vector<Eigen::Triplet<double>> m_cachedTriplets;

  // List of row indices for nonlinear rows whose graients will be computed in
  // Value()
  small_vector<int> m_nonlinearRows;

  Profiler m_profiler;
};

}  // namespace sleipnir
