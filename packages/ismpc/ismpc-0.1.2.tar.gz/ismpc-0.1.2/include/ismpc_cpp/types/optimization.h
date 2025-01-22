#pragma once

#include <iostream>

#include "ismpc_cpp/types/math_types.h"

namespace ismpc {

struct Cost {
    Matrix H;
    VectorX g;

    Cost() = default;
    Cost(Matrix H, VectorX g) : H(H), g(g){};
    Cost(int d) : H(Matrix::Zero(d, d)), g(VectorX::Zero(d)){};

    friend std::ostream& operator<<(std::ostream& os, const Cost& cost) {
        os << "H:\n" << cost.H << "\ng:\n" << cost.g << "\n";
        return os;
    }

    void validateMatrices() const {
        if (H.maxCoeff() > 1e6 || H.minCoeff() < 1e-6) {
            std::cout << "Warning: H matrix poorly scaled\n";
        }

        if (g.maxCoeff() > 1e6 || H.minCoeff() < 1e-6) {
            std::cout << "Warning: g vector poorly scaled\n";
        }
    }
};

struct InequalityConstraint {
    Matrix C;
    VectorX l;
    VectorX u;

    InequalityConstraint() = default;
    InequalityConstraint(Matrix C, VectorX l, VectorX u) : C(C), l(l), u(u){};
    InequalityConstraint(int n_in, int d)
        : C(Matrix::Zero(n_in, d)), l(VectorX::Zero(n_in)), u(VectorX::Zero(n_in)){};

    friend std::ostream& operator<<(std::ostream& os, const InequalityConstraint& inequality) {
        Eigen::IOFormat HeavyFmt(Eigen::FullPrecision, 0, ", ", ";\n", "[", "]", "[", "]");
        os << "C:\n"
           << inequality.C.format(HeavyFmt) << "\nl:\n"
           << inequality.l.format(HeavyFmt) << "\nu:\n"
           << inequality.u.format(HeavyFmt) << "\n";
        return os;
    }

    void validateMatrices() const {
        if (C.maxCoeff() > 1e6) {
            std::cout << "Warning: C matrix poorly scaled\n";
        }

        if ((u - l).minCoeff() < 1e-10) {
            std::cout << "Warning: Tight/inconsistent bounds\n";
        }
    }
};

struct EqualityConstraint {
    Matrix A;
    VectorX b;

    EqualityConstraint() = default;
    EqualityConstraint(Matrix A, VectorX b) : A(A), b(b){};
    EqualityConstraint(int n_eq, int d) : A(Matrix::Zero(n_eq, d)), b(VectorX::Zero(n_eq)){};

    friend std::ostream& operator<<(std::ostream& os, const EqualityConstraint& equality) {
        os << "A:\n" << equality.A << "\nb:\n" << equality.b << "\n";
        return os;
    }

    void validateMatrices() const {
        if (A.maxCoeff() > 1e6) {
            std::cout << "Warning: A matrix poorly scaled\n";
        }

        if (b.maxCoeff() > 1e6) {
            std::cout << "Warning: b vector poorly scaled\n";
        }
    }
};

}  // namespace ismpc
