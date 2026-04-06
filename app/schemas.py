from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )

    description = fields.Str(
        required=False,
        validate=validate.Length(max=500)
    )

    completed = fields.Bool(
        load_default=False,
        dump_default=False
    )

    due_date = fields.DateTime(
        format='iso',
        required=False
    )

    category_id = fields.Int(
        required=False
    )

    created_at = fields.DateTime(
        dump_only=True
    )

    updated_at = fields.DateTime(
        dump_only=True
    )

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )

    color = fields.Str(
        required=False,
        validate=[
            validate.Length(equal=7),
            validate.Regexp(r'^#[0-9A-Fa-f]{6}$')
        ]
    )