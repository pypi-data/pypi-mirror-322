use pyo3::{exceptions::PyException, prelude::*};
use std::collections::HashMap;
use tokio::runtime::Runtime;
use topk_protos::v1::control::Index;
use topk_sdk_core::ClientConfig;

struct CoreError(topk_sdk_core::Error);

impl From<CoreError> for PyErr {
    fn from(error: CoreError) -> Self {
        PyException::new_err(format!("{:?}", error.0))
    }
}

impl From<topk_sdk_core::Error> for CoreError {
    fn from(other: topk_sdk_core::Error) -> Self {
        Self(other)
    }
}

#[pyclass]
struct Client {
    runtime: Runtime,
    config: ClientConfig,
}

#[pymethods]
impl Client {
    #[new]
    #[pyo3(signature = (api_key, region=None))]
    fn new(api_key: String, region: Option<String>) -> Self {
        let runtime = Runtime::new().unwrap();

        Self {
            runtime,
            config: ClientConfig { api_key, region },
        }
    }

    fn create_index(&self, index_name: String, schema: HashMap<String, String>) -> PyResult<()> {
        println!(
            "Creating index {} with schema {:?} with api key {} and region {:?}",
            index_name, schema, self.config.api_key, self.config.region
        );
        Ok(())
    }

    fn upsert(&self, index_name: String, documents: Vec<HashMap<String, Scalar>>) -> PyResult<u64> {
        Ok(self.runtime.block_on(async move {
            topk_sdk_core::Client::new(self.config.api_key.clone(), self.config.region.clone())
                .upsert(
                    topk_protos::v1::control::Index {
                        name: index_name,
                        org_id: 1,
                        project_id: 1,
                        schema: HashMap::new(),
                    },
                    documents
                        .into_iter()
                        .map(|d| topk_protos::v1::data::Document {
                            fields: d.into_iter().map(|(k, v)| (k, v.into())).collect(),
                        })
                        .collect(),
                )
                .await
                .map_err(CoreError)
        })?)
    }

    fn query(&self, query: Query) -> PyResult<()> {
        let qq: topk_protos::v1::data::Query = {
            topk_protos::v1::data::Query {
                stages: query.stages.into_iter().map(|s| s.into()).collect(),
            }
        };

        tokio::runtime::Runtime::new()
            .unwrap()
            .block_on(async move {
                let aa = topk_sdk_core::Client::new(
                    self.config.api_key.clone(),
                    self.config.region.clone(),
                )
                .query(
                    Index {
                        name: "test".to_string(),
                        org_id: 1,
                        project_id: 1,
                        schema: HashMap::new(),
                    },
                    qq,
                )
                .await
                .unwrap();

                println!("aa: {:?}", aa);
            });

        Ok(())
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum BinaryOperator {
    // Logical ops
    And,
    Or,
    Xor,
    // Comparison ops
    Eq,
    NotEq,
    Lt,
    LtEq,
    Gt,
    GtEq,
    // Arithmetic ops
    Add,
    Sub,
    Mul,
    Div,
    Rem,
}

#[derive(Debug, Clone, PartialEq, FromPyObject, IntoPyObject)]
pub enum Scalar {
    Bool(bool),
    Int(i64),
    Float(f64),
    String(String),
}

#[pyclass]
#[derive(Debug, Clone)]
enum Expression {
    Field {
        name: String,
    },
    Literal {
        value: Scalar,
    },
    // Unary {
    //     op: UnaryOperator,
    //     expr: Arc<Expr>,
    // },
    Binary {
        left: Py<Expression>,
        op: BinaryOperator,
        right: Py<Expression>,
    },
    // Nary {
    //     op: NaryOperator,
    //     exprs: Vec<Arc<Expr>>,
    // },
}

#[pymethods]
impl Expression {
    fn __add__(&self, py: Python<'_>, other: Py<Expression>) -> PyResult<Self> {
        Ok(Self::Binary {
            left: Py::new(py, self.clone())?,
            op: BinaryOperator::Add,
            right: Py::new(py, other.clone())?,
        })
    }

    fn __radd__(&self, py: Python<'_>, other: Py<Expression>) -> PyResult<Self> {
        Ok(Self::Binary {
            left: Py::new(py, other.clone())?,
            op: BinaryOperator::Add,
            right: Py::new(py, self.clone())?,
        })
    }

    fn __and__(&self, py: Python<'_>, other: Py<Expression>) -> PyResult<Self> {
        Ok(Self::Binary {
            left: Py::new(py, self.clone())?,
            op: BinaryOperator::And,
            right: Py::new(py, other.clone())?,
        })
    }

    fn __or__(&self, py: Python<'_>, other: Py<Expression>) -> PyResult<Self> {
        Ok(Self::Binary {
            left: Py::new(py, self.clone())?,
            op: BinaryOperator::Or,
            right: Py::new(py, other.clone())?,
        })
    }

    fn eq(&self, py: Python<'_>, other: Py<Expression>) -> PyResult<Self> {
        Ok(Self::Binary {
            left: Py::new(py, self.clone())?,
            op: BinaryOperator::Eq,
            right: Py::new(py, other.clone())?,
        })
    }

    fn neq(&self, py: Python<'_>, other: Py<Expression>) -> PyResult<Self> {
        Ok(Self::Binary {
            left: Py::new(py, self.clone())?,
            op: BinaryOperator::NotEq,
            right: Py::new(py, other.clone())?,
        })
    }
}

#[pyclass]
#[derive(Debug, Clone)]
enum Stage {
    Select {
        exprs: HashMap<String, Py<Expression>>,
    },
    Filter {
        expr: Py<Expression>,
    },
    TopK {
        expr: Py<Expression>,
        k: usize,
        asc: bool,
    },
}

impl Into<topk_protos::v1::data::Value> for Scalar {
    fn into(self) -> topk_protos::v1::data::Value {
        topk_protos::v1::data::Value {
            value: Some(match self {
                Scalar::Bool(b) => topk_protos::v1::data::value::Value::Bool(b),
                Scalar::Int(i) => topk_protos::v1::data::value::Value::I64(i),
                Scalar::Float(f) => topk_protos::v1::data::value::Value::F64(f),
                Scalar::String(s) => topk_protos::v1::data::value::Value::String(s),
            }),
        }
    }
}

impl Into<topk_protos::v1::data::Stage> for Stage {
    fn into(self) -> topk_protos::v1::data::Stage {
        match self {
            Stage::Select { exprs } => topk_protos::v1::data::Stage {
                stage: Some(topk_protos::v1::data::stage::Stage::Select(
                    topk_protos::v1::data::stage::SelectStage {
                        exprs: exprs
                            .into_iter()
                            .map(|(k, v)| (k, v.get().into()))
                            .collect(),
                    },
                )),
            },
            Stage::Filter { expr } => topk_protos::v1::data::Stage {
                stage: Some(topk_protos::v1::data::stage::Stage::Filter(
                    topk_protos::v1::data::stage::FilterStage {
                        expr: Some(topk_protos::v1::data::stage::filter_stage::FilterExpr {
                            expr: Some(expr.get().into()),
                        }),
                    },
                )),
            },
            Stage::TopK { expr, k, asc } => topk_protos::v1::data::Stage {
                stage: Some(topk_protos::v1::data::stage::Stage::TopK(
                    topk_protos::v1::data::stage::TopKStage {
                        expr: Some(expr.get().into()),
                        k: k as u64,
                        asc,
                    },
                )),
            },
        }
    }
}

impl Into<topk_protos::v1::data::stage::filter_stage::filter_expr::Expr> for &Expression {
    fn into(self) -> topk_protos::v1::data::stage::filter_stage::filter_expr::Expr {
        topk_protos::v1::data::stage::filter_stage::filter_expr::Expr::LogicalExpr(self.into())
    }
}

impl Into<topk_protos::v1::data::stage::select_stage::SelectExpr> for &Expression {
    fn into(self) -> topk_protos::v1::data::stage::select_stage::SelectExpr {
        topk_protos::v1::data::stage::select_stage::SelectExpr {
            expr: Some(
                topk_protos::v1::data::stage::select_stage::select_expr::Expr::LogicalExpr(
                    topk_protos::v1::data::LogicalExpr {
                        expr: Some(self.into()),
                    },
                ),
            ),
        }
    }
}

impl Into<topk_protos::v1::data::LogicalExpr> for &Expression {
    fn into(self) -> topk_protos::v1::data::LogicalExpr {
        topk_protos::v1::data::LogicalExpr {
            expr: Some(self.into()),
        }
    }
}

impl Into<topk_protos::v1::data::logical_expr::Expr> for &Expression {
    fn into(self) -> topk_protos::v1::data::logical_expr::Expr {
        match self {
            Expression::Field { name } => {
                topk_protos::v1::data::logical_expr::Expr::Field(name.clone())
            }
            Expression::Literal { value } => {
                topk_protos::v1::data::logical_expr::Expr::Literal(value.into())
            }
            Expression::Binary { left, op, right } => {
                let op: topk_protos::v1::data::logical_expr::binary_op::Op = op.into();

                topk_protos::v1::data::logical_expr::Expr::BinaryOp(Box::new(
                    topk_protos::v1::data::logical_expr::BinaryOp {
                        op: op as i32,
                        left: Some(Box::new(left.get().into())),
                        right: Some(Box::new(right.get().into())),
                    },
                ))
            }
            _ => unreachable!(),
        }
    }
}

impl Into<topk_protos::v1::data::logical_expr::binary_op::Op> for &BinaryOperator {
    fn into(self) -> topk_protos::v1::data::logical_expr::binary_op::Op {
        match self {
            BinaryOperator::Eq => topk_protos::v1::data::logical_expr::binary_op::Op::Eq,
            BinaryOperator::NotEq => topk_protos::v1::data::logical_expr::binary_op::Op::Neq,
            BinaryOperator::Lt => topk_protos::v1::data::logical_expr::binary_op::Op::Lt,
            BinaryOperator::LtEq => topk_protos::v1::data::logical_expr::binary_op::Op::Lte,
            BinaryOperator::Gt => topk_protos::v1::data::logical_expr::binary_op::Op::Gt,
            BinaryOperator::GtEq => topk_protos::v1::data::logical_expr::binary_op::Op::Gte,
            BinaryOperator::Add => topk_protos::v1::data::logical_expr::binary_op::Op::Add,
            BinaryOperator::Sub => topk_protos::v1::data::logical_expr::binary_op::Op::Sub,
            BinaryOperator::Mul => topk_protos::v1::data::logical_expr::binary_op::Op::Mul,
            BinaryOperator::Div => topk_protos::v1::data::logical_expr::binary_op::Op::Div,
            BinaryOperator::And => topk_protos::v1::data::logical_expr::binary_op::Op::And,
            BinaryOperator::Or => topk_protos::v1::data::logical_expr::binary_op::Op::Or,
            _ => unreachable!(),
        }
    }
}

impl Into<topk_protos::v1::data::Value> for &Scalar {
    fn into(self) -> topk_protos::v1::data::Value {
        topk_protos::v1::data::Value {
            value: Some(match self {
                Scalar::Bool(b) => topk_protos::v1::data::value::Value::Bool(*b),
                Scalar::Int(i) => topk_protos::v1::data::value::Value::I64(*i),
                Scalar::Float(f) => topk_protos::v1::data::value::Value::F64(*f),
                Scalar::String(s) => topk_protos::v1::data::value::Value::String(s.clone()),
            }),
        }
    }
}

#[pyclass]
#[derive(Debug, Clone)]
struct Query {
    collection: String,
    stages: Vec<Stage>,
}

#[pymethods]
impl Query {
    #[pyo3(signature = (*args, **kwargs))]
    fn select(
        &self,
        py: Python<'_>,
        args: Vec<String>,
        kwargs: Option<HashMap<String, Py<Expression>>>,
    ) -> PyResult<Self> {
        let exprs = {
            let mut exprs = HashMap::new();

            // apply `*args`
            for arg in args {
                exprs.insert(arg.clone(), Py::new(py, field(arg)?)?);
            }

            // apply `**kwargs`
            for (key, value) in kwargs.unwrap_or_default() {
                exprs.insert(key.clone(), value);
            }

            exprs
        };

        Ok(Self {
            collection: self.collection.clone(),
            stages: [self.stages.clone(), vec![Stage::Select { exprs }]].concat(),
        })
    }

    fn filter(&self, expr: Py<Expression>) -> PyResult<Self> {
        Ok(Self {
            collection: self.collection.clone(),
            stages: [self.stages.clone(), vec![Stage::Filter { expr }]].concat(),
        })
    }

    #[pyo3(signature = (expr, k, asc=false))]
    fn top_k(&self, expr: Py<Expression>, k: usize, asc: bool) -> PyResult<Self> {
        Ok(Self {
            collection: self.collection.clone(),
            stages: [self.stages.clone(), vec![Stage::TopK { expr, k, asc }]].concat(),
        })
    }
}

#[pyfunction]
fn collection(name: String) -> PyResult<Query> {
    Ok(Query {
        collection: name,
        stages: vec![],
    })
}

#[pyfunction]
fn field(name: String) -> PyResult<Expression> {
    Ok(Expression::Field { name })
}

#[pyfunction]
fn literal(value: Scalar) -> PyResult<Expression> {
    Ok(Expression::Literal { value })
}

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name = "_topk_sdk")]
fn topk_sdk(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(collection, m)?)?;
    m.add_function(wrap_pyfunction!(field, m)?)?;
    m.add_function(wrap_pyfunction!(literal, m)?)?;

    m.add_class::<Client>()?;

    Ok(())
}
