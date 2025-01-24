use super::*;
use crate::v1::data;
use index_schema::IndexSchema;

#[derive(Debug, thiserror::Error, PartialEq, Eq)]
pub enum DocumentValidationError {
    #[error("Document _id must be a non empty string")]
    InvalidId,

    #[error("Document must have an _id field")]
    MissingId,

    #[error("Document must have a field [{field}]")]
    MissingField { field: String },

    #[error("Field name `{field}` cannot start with underscore")]
    ReservedFieldName { field: String },

    #[error("Document contains an invalid data type for field [{field}]")]
    InvalidDataType { field: String },

    #[error("No documents provided")]
    NoDocuments,
}

pub fn validate_documents(
    schema: &IndexSchema,
    documents: &[data::Document],
) -> Result<(), Vec<DocumentValidationError>> {
    let mut errors = vec![];

    if documents.is_empty() {
        return Err(vec![DocumentValidationError::NoDocuments]);
    }

    for doc in documents {
        // Validate `_id` field
        match doc.fields.get("_id") {
            Some(id) => match &id.value {
                Some(data::value::Value::String(id)) if !id.is_empty() => {}
                _ => {
                    errors.push(DocumentValidationError::InvalidId);
                }
            },
            None => {
                errors.push(DocumentValidationError::MissingId);
            }
        }

        // Validate reserved field names
        for key in doc.fields.keys() {
            if key.starts_with("_") && key != "_id" {
                errors.push(DocumentValidationError::ReservedFieldName { field: key.clone() });
            }
        }

        // Validate required fields
        for (key, spec) in schema.fields() {
            if spec.required && doc.fields.get(key).is_none() {
                errors.push(DocumentValidationError::MissingField { field: key.clone() });
            }
        }

        // Validate data types
        for (key, spec) in schema.fields() {
            match (spec.data_type, doc.fields.get(key)) {
                (
                    Some(FieldType {
                        data_type: Some(ref dt),
                    }),
                    Some(data::Value { value: Some(v) }),
                ) => {
                    if !types_match(dt, v) {
                        errors
                            .push(DocumentValidationError::InvalidDataType { field: key.clone() });
                    }
                }
                _ => {}
            }
        }
    }

    if !errors.is_empty() {
        return Err(errors);
    }

    Ok(())
}

pub fn validate_document_ids(ids: &[String]) -> Result<(), Vec<DocumentValidationError>> {
    if ids.is_empty() {
        return Err(vec![DocumentValidationError::NoDocuments]);
    }

    for id in ids {
        if id.is_empty() {
            return Err(vec![DocumentValidationError::InvalidId]);
        }
    }

    Ok(())
}

fn types_match(spec: &field_type::DataType, value: &data::value::Value) -> bool {
    match (spec, value) {
        (field_type::DataType::Text(..), data::value::Value::String(..)) => true,
        (field_type::DataType::Integer(..), data::value::Value::U32(..)) => true,
        (field_type::DataType::Integer(..), data::value::Value::I32(..)) => true,
        (field_type::DataType::Integer(..), data::value::Value::U64(..)) => true,
        (field_type::DataType::Integer(..), data::value::Value::I64(..)) => true,
        (field_type::DataType::Float(..), data::value::Value::F32(..)) => true,
        (field_type::DataType::Float(..), data::value::Value::F64(..)) => true,
        (field_type::DataType::Boolean(..), data::value::Value::Bool(..)) => true,
        (field_type::DataType::Bytes(..), data::value::Value::Binary(..)) => true,
        (field_type::DataType::FloatVector(dt), data::value::Value::Vector(v)) => match v.len() {
            Some(len) => dt.dimension == len as u32,
            None => false,
        },
        (field_type::DataType::ByteVector(dt), data::value::Value::Vector(v)) => match v.len() {
            Some(len) => dt.dimension == len as u32,
            None => false,
        },
        _ => false,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::v1::control::{
        field_type::DataType, FieldType, FieldTypeBoolean, FieldTypeBytes, FieldTypeFloat,
        FieldTypeInteger, FieldTypeText,
    };
    use std::collections::HashMap;

    #[test]
    fn test_validate_empty_documents() {
        let errors = validate_documents(&IndexSchema::default(), &vec![]).expect_err("should fail");

        assert_eq!(errors, vec![DocumentValidationError::NoDocuments]);
    }

    #[test]
    fn test_validate_documents_missing_id() {
        let errors = validate_documents(
            &IndexSchema::default(),
            &[data::Document {
                fields: HashMap::new(),
            }],
        )
        .expect_err("should fail");

        assert_eq!(errors, vec![DocumentValidationError::MissingId]);
    }

    #[test]
    fn test_validate_documents_wrong_id_type() {
        let errors = validate_documents(
            &IndexSchema::default(),
            &vec![data::Document::from([
                ("_id", data::Value::u32(1)),
                ("data", data::Value::string("x".repeat(1 * 1024))),
            ])],
        )
        .expect_err("should fail");

        assert_eq!(errors, vec![DocumentValidationError::InvalidId]);
    }

    #[test]
    fn test_validate_documents_reserved_field_name() {
        let errors = validate_documents(
            &IndexSchema::default(),
            &vec![data::Document::from([
                ("_id", data::Value::string("1".to_string())),
                ("_reserved", data::Value::string("foo".to_string())),
            ])],
        )
        .expect_err("reserved field");

        assert_eq!(
            errors,
            vec![DocumentValidationError::ReservedFieldName {
                field: "_reserved".to_string()
            }]
        );
    }

    #[test]
    fn test_validate_documents_missing_field() {
        let errors = validate_documents(
            &IndexSchema::try_from([(
                "age".to_string(),
                FieldSpec {
                    data_type: Some(FieldType {
                        data_type: Some(DataType::Integer(FieldTypeInteger {})),
                    }),
                    required: true,
                    index: None,
                },
            )])
            .unwrap(),
            &vec![data::Document::from([(
                "_id",
                data::Value::string("1".to_string()),
            )])],
        )
        .expect_err("should fail");

        assert_eq!(
            errors,
            vec![DocumentValidationError::MissingField {
                field: "age".to_string()
            }]
        );
    }

    #[rstest::rstest]
    #[case(DataType::Integer(FieldTypeInteger {}), data::Value::string("foo".to_string()))]
    #[case(DataType::Text(FieldTypeText {}), data::Value::u32(3))]
    #[case(DataType::Float(FieldTypeFloat {}), data::Value::u32(3))]
    #[case(DataType::Boolean(FieldTypeBoolean {}), data::Value::u32(3))]
    #[case(DataType::Bytes(FieldTypeBytes {}), data::Value::u32(3))]
    #[case(DataType::FloatVector(FieldTypeFloatVector { dimension: 3 }), data::Value::binary(vec![0,1,2]))]
    #[case(DataType::ByteVector(FieldTypeByteVector { dimension: 3 }), data::Value::binary(vec![0,1,2]))]
    fn test_validate_documents_invalid_data_type(
        #[case] data_type: DataType,
        #[case] value: data::Value,
    ) {
        let errors = validate_documents(
            &IndexSchema::try_from([(
                "field".to_string(),
                FieldSpec {
                    data_type: Some(FieldType {
                        data_type: Some(data_type),
                    }),
                    required: true,
                    index: None,
                },
            )])
            .unwrap(),
            &vec![data::Document::from([
                ("_id", data::Value::string("1".to_string())),
                ("field", value),
            ])],
        )
        .expect_err("should fail");

        assert_eq!(
            errors,
            vec![DocumentValidationError::InvalidDataType {
                field: "field".to_string()
            }]
        );
    }

    #[test]
    fn test_validate_wrong_vector_dimension() {
        let errors = validate_documents(
            &IndexSchema::try_from([(
                "field",
                FieldSpec {
                    data_type: Some(FieldType {
                        data_type: Some(DataType::FloatVector(FieldTypeFloatVector {
                            dimension: 3,
                        })),
                    }),
                    required: true,
                    index: None,
                },
            )])
            .unwrap(),
            &vec![data::Document::from([
                ("_id", data::Value::string("1".to_string())),
                ("field", data::Value::float_vector(vec![0.0, 1.0, 2.0, 3.0])),
            ])],
        )
        .expect_err("should fail");

        assert_eq!(
            errors,
            vec![DocumentValidationError::InvalidDataType {
                field: "field".to_string()
            }]
        );
    }

    #[test]
    fn test_validate_document_ids_no_documents() {
        let errors = validate_document_ids(&vec![]).expect_err("should fail");

        assert_eq!(errors, vec![DocumentValidationError::NoDocuments]);
    }

    #[test]
    fn test_validate_document_ids_empty() {
        let errors = validate_document_ids(&vec!["".to_string()]).expect_err("should fail");

        assert_eq!(errors, vec![DocumentValidationError::InvalidId]);
    }
}
