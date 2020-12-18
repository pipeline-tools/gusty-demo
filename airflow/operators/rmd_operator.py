from airflow.operators.bash_operator import BashOperator
from airflow.utils.decorators import apply_defaults

command_template = """
Rscript -e 'rmarkdown::render("{file_path}", run_pandoc=FALSE)' || exit 1; rm -f {rendered_output}
"""

class RmdOperator(BashOperator):
    """
    The LocalRmdOperator executes the R Markdown file.
    Note that it is up to the Rmd itself to handle connecting to a database.
    """
    ui_color = "#75AADB"
    template_fields = BashOperator.template_fields + ('file_path', )

    # gusty gives us a file_path for free
    @apply_defaults
    def __init__(self, file_path, *args, **kwargs):
        self.file_path = file_path
        self.rendered_output = self.file_path.replace('.Rmd', '.knit.md')

        command = command_template.format(file_path = self.file_path,
                                          rendered_output = self.rendered_output)

        super(RmdOperator, self).__init__(bash_command = command, *args, **kwargs)

    def execute(self, context):
        super(RmdOperator, self).execute(context)
