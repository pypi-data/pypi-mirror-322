use super::*;

impl Document {
    /// Returns document _id field.
    ///
    /// ## Panics
    /// - if the _id field is missing
    /// - if the _id field is not [`String`](value::Value::String)
    #[inline]
    pub fn id(&self) -> &str {
        match self.fields.get("_id").map(|v| &v.value) {
            Some(Some(val)) => match val {
                value::Value::String(id) => id,
                _ => panic!("Invalid document _id field"),
            },
            _ => panic!("Missing document _id field"),
        }
    }
}

impl<const N: usize> From<[(&str, Value); N]> for Document {
    fn from(entries: [(&str, Value); N]) -> Self {
        let fields = entries
            .into_iter()
            .map(|(k, v)| (k.to_string(), v))
            .collect();
        Document { fields }
    }
}
