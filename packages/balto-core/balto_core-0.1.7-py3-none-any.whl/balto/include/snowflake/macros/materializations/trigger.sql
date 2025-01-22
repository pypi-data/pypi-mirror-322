{% materialization trigger, adapter='snowflake' -%}

    {% set original_query_tag = set_query_tag() %}
    {% set to_return = snowflake__create_or_replace_view() %}

    {% set identifier = model['alias'] -%}
    {% set identifier_temp_table = identifier + '_temp_table' -%}
    {% set identifier_stream = identifier + '_stream' -%}
    {% set identifier_task = identifier + '_task' -%}

    {% set target_relation = this.incorporate(type='view') %}
    {% set target_temp_table = api.Relation.create(database=database, schema=schema, identifier=identifier_temp_table) %}
    {% set target_stream = api.Relation.create(database=database, schema=schema, identifier=identifier_stream) %}
    {% set target_task = api.Relation.create(database=database, schema=schema, identifier=identifier_task) %}

    {% call statement('create_stream') -%}
        CREATE OR REPLACE STREAM {{ target_stream }} ON VIEW {{ target_relation }};
    {% endcall -%}

    {% call statement('create_task') -%}
        CALL dbt.create_trigger(
            '{{ project_name }}',
            '{{ identifier }}',
            '{{ target_stream }}',
            '{{ model['config']['handler'] }}',
            '{{ model['config']['enabled'] }}'
        );
    {% endcall -%}

    {% do persist_docs(target_relation, model, for_columns=false) %}

    {% do unset_query_tag(original_query_tag) %}

    {% do return(to_return) %}

{%- endmaterialization %}
