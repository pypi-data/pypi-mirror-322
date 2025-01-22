{% materialization schedule, adapter='snowflake' %}
    {%- set identifier = model['alias'] -%}

    {% call statement('main') -%}
        CALL dbt.create_scheduled_build(
            '{{ project_name }}',
            '{{ identifier }}',
            '{{ model['schedule'] }}',
            '{{ model['selector'] }}',
            '{{ model['config']['enabled'] }}'
        );
    {% endcall -%}

    {{ return({'relations': []}) }}
{% endmaterialization %}
