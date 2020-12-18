from airflow.operators.bash_operator import BashOperator
from airflow.utils.decorators import apply_defaults

command_template = """
jupyter nbconvert --to html --execute {file_path} || exit 1; rm -f {rendered_output}
"""

class JupyterOperator(BashOperator):
    """
    The LocalJupyterOperator executes the Jupyter Notebook.
    Note that it is up to the notebook itself to handle connecting to a database.
    (But it can grab this from airflow connections)
    """
    ui_color = "#EF8D50"
    template_fields = BashOperator.template_fields + ('file_path', )

    # gusty gives us a file_path for free
    @apply_defaults
    def __init__(self, file_path, *args, **kwargs):
        self.file_path = file_path
        self.rendered_output = self.file_path.replace('.ipynb', '.html')

        command = command_template.format(file_path = self.file_path,
                                          rendered_output = self.rendered_output)

        super(JupyterOperator, self).__init__(bash_command = command, *args, **kwargs)

    def execute(self, context):
        super(JupyterOperator, self).execute(context)
