{% macro transfer_ownership(database, schema, application_name="balto") %}
    {% set clone_query %}
    CALL {{ application_name }}.config.clone_objects('{{ database }}', '{{ schema }}')
    {% endset %}

    {% set clone_results = run_query(clone_query) %}

    {% for cloned_obj in clone_results.rows %}
        {% set object_kind = "" %}

        {% if cloned_obj["KIND"] == "TABLE" and cloned_obj["IS_DYNAMIC"] == "Y" %}
            {% set object_kind = "DYNAMIC TABLE" %}
        {% elif cloned_obj["KIND"] == "TABLE" and cloned_obj["IS_DYNAMIC"] != "Y" %}
            {% set object_kind = "TABLE" %}
        {% elif cloned_obj["KIND"] == "VIEW" %}
            {% set object_kind = "VIEW" %}
        {% endif %}

        {% set drop_query %}
        DROP {{ object_kind }} {{ database }}.{{ schema }}.{{ cloned_obj["NAME"] }}
        {% endset %}

        {% set drop_results = run_query(drop_query) %}
    {% endfor %}

    {% set rename_query %}
    CALL {{ application_name }}.config.rename_cloned_objects('{{ database }}', '{{ schema }}')
    {% endset %}

    {% set rename_results = run_query(rename_query) %}
{% endmacro %}
