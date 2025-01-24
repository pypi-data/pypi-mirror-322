use super::*;

impl Value {
    pub fn null() -> Self {
        Value { value: None }
    }

    pub fn bool(value: bool) -> Self {
        Value {
            value: Some(value::Value::Bool(value)),
        }
    }

    pub fn string(value: impl Into<String>) -> Self {
        Value {
            value: Some(value::Value::String(value.into())),
        }
    }

    pub fn u32(value: u32) -> Self {
        Value {
            value: Some(value::Value::U32(value)),
        }
    }

    pub fn u64(value: u64) -> Self {
        Value {
            value: Some(value::Value::U64(value)),
        }
    }

    pub fn i32(value: i32) -> Self {
        Value {
            value: Some(value::Value::I32(value)),
        }
    }

    pub fn i64(value: i64) -> Self {
        Value {
            value: Some(value::Value::I64(value)),
        }
    }

    pub fn f32(value: f32) -> Self {
        Value {
            value: Some(value::Value::F32(value)),
        }
    }

    pub fn f64(value: f64) -> Self {
        Value {
            value: Some(value::Value::F64(value)),
        }
    }

    pub fn float_vector(values: Vec<f32>) -> Self {
        Value {
            value: Some(value::Value::Vector(Vector {
                vector: Some(vector::Vector::Float(vector::Float { values })),
            })),
        }
    }

    pub fn byte_vector(values: Vec<u8>) -> Self {
        Value {
            value: Some(value::Value::Vector(Vector {
                vector: Some(vector::Vector::Byte(vector::Byte { values })),
            })),
        }
    }

    pub fn binary(value: Vec<u8>) -> Self {
        Value {
            value: Some(value::Value::Binary(value)),
        }
    }
}

impl From<String> for Value {
    fn from(value: String) -> Self {
        Value::string(value)
    }
}

impl From<&str> for Value {
    fn from(value: &str) -> Self {
        Value::string(value.to_string())
    }
}

impl From<u32> for Value {
    fn from(value: u32) -> Self {
        Value::u32(value)
    }
}

impl From<u64> for Value {
    fn from(value: u64) -> Self {
        Value::u64(value)
    }
}

impl From<i32> for Value {
    fn from(value: i32) -> Self {
        Value::i32(value)
    }
}

impl From<i64> for Value {
    fn from(value: i64) -> Self {
        Value::i64(value)
    }
}

impl From<f32> for Value {
    fn from(value: f32) -> Self {
        Value::f32(value)
    }
}

impl From<f64> for Value {
    fn from(value: f64) -> Self {
        Value::f64(value)
    }
}

impl From<Vec<f32>> for Value {
    fn from(value: Vec<f32>) -> Self {
        Value::float_vector(value)
    }
}

impl From<bool> for Value {
    fn from(value: bool) -> Self {
        Value::bool(value)
    }
}

impl From<Vec<u8>> for Value {
    fn from(value: Vec<u8>) -> Self {
        Value::binary(value)
    }
}

impl Vector {
    pub fn float(values: Vec<f32>) -> Self {
        Vector {
            vector: Some(vector::Vector::Float(vector::Float { values })),
        }
    }

    pub fn byte(values: Vec<u8>) -> Self {
        Vector {
            vector: Some(vector::Vector::Byte(vector::Byte { values })),
        }
    }

    pub fn len(&self) -> Option<usize> {
        match &self.vector {
            Some(vector::Vector::Float(vector::Float { values })) => Some(values.len()),
            Some(vector::Vector::Byte(vector::Byte { values })) => Some(values.len()),
            _ => None,
        }
    }
}
