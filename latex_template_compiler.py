import os
import subprocess

from jinja2 import Environment, FileSystemLoader, meta
from dotenv import dotenv_values


def render_latex_pdf(**context):
    try:
        config = dotenv_values(".env")
        TEX_TEMPLATE_PATH = config["TEX_TEMPLATE_PATH"]
        RENDERED_TEX_PATH = config["RENDERED_TEX_PATH"]
        PDF_PATH = config["PDF_PATH"]
        if TEX_TEMPLATE_PATH is None:
            raise Exception("TEX_TEMPLATE_PATH not found. Check your .env file.")
        if RENDERED_TEX_PATH is None:
            raise Exception("RENDERED_TEX_PATH not found. Check your .env file.")
        if PDF_PATH is None:
            raise Exception("PDF_PATH not found. Check your .env file.")
        # Todo: if path does not exist create it instead of raising exception?
        if not os.path.exists(TEX_TEMPLATE_PATH):
            raise FileNotFoundError("%s path Does Not Exist." % TEX_TEMPLATE_PATH)
        if not os.path.exists(RENDERED_TEX_PATH):
            raise FileNotFoundError("%s path Does Not Exist." % RENDERED_TEX_PATH)
        if not os.path.exists(PDF_PATH):
            raise FileNotFoundError("%s path Does Not Exist." % PDF_PATH)
    except Exception as e:
        # Todo: instead of raising maybe creating the files will be better?
        return e.message
    else:
        env = Environment(loader=FileSystemLoader(TEX_TEMPLATE_PATH),
                          block_start_string='<BLOCK>',
                          block_end_string='</BLOCK>',
                          variable_start_string='<VAR>',
                          variable_end_string='</VAR>',
                          comment_start_string='<COMMENT>',
                          comment_end_string='</COMMENT>',
                          )

        # Todo: template name is hardcoded need to change

        template_name = env.list_templates()[0]
        if template_name:
            template = env.get_template(template_name)

            # Todo: render needs context of dict.
            tex_string = template.render(context)
        else:
            raise Exception("Template Not Found")

        with open(os.path.join(RENDERED_TEX_PATH, template_name), "w") as template_file:
            template_file.write(tex_string)

        try:
            # assuming that docker container for pdflatex image is running
            # Todo: need to check that container is running before start?
            container_name = "latex_server2"  # Todo: make it dynamic
            # Todo: make the whole subprocess runner dynamic a function call as most of the command should be static only
            #  thing that will change will be source and output files
            subprocess.run(["docker", "exec", container_name, "pdflatex", "--output-directory=./%s" % PDF_PATH,
                            "./%s/%s" % (RENDERED_TEX_PATH, template_name)], check=True)
        except Exception as e:
            return e.message
        else:
            return os.path.join(PDF_PATH, template_name.replace(".tex", ".pdf"))


def get_required_context():
    try:
        config = dotenv_values(".env")
        TEX_TEMPLATE_PATH = config["TEX_TEMPLATE_PATH"]
        RENDERED_TEX_PATH = config["RENDERED_TEX_PATH"]
        PDF_PATH = config["PDF_PATH"]
        if TEX_TEMPLATE_PATH is None:
            raise Exception("TEX_TEMPLATE_PATH not found. Check your .env file.")
        if RENDERED_TEX_PATH is None:
            raise Exception("RENDERED_TEX_PATH not found. Check your .env file.")
        if PDF_PATH is None:
            raise Exception("PDF_PATH not found. Check your .env file.")
        # Todo: if path does not exist create it instead of raising exception?
        if not os.path.exists(TEX_TEMPLATE_PATH):
            raise FileNotFoundError("%s path Does Not Exist." % TEX_TEMPLATE_PATH)
        if not os.path.exists(RENDERED_TEX_PATH):
            raise FileNotFoundError("%s path Does Not Exist." % RENDERED_TEX_PATH)
        if not os.path.exists(PDF_PATH):
            raise FileNotFoundError("%s path Does Not Exist." % PDF_PATH)
    except Exception as e:
        # Todo: instead of raising maybe creating the files will be better?
        return e.message
    else:
        env = Environment(loader=FileSystemLoader(TEX_TEMPLATE_PATH),
                          block_start_string='<BLOCK>',
                          block_end_string='</BLOCK>',
                          variable_start_string='<VAR>',
                          variable_end_string='</VAR>',
                          comment_start_string='<COMMENT>',
                          comment_end_string='</COMMENT>',
                          )

        # Todo: template name is hardcoded need to change

        template_name = env.list_templates()[0]
        if template_name:
            template_source = env.loader.get_source(env, template_name)[0]
            template_ats = env.parse(template_source)
            required_context = meta.find_undeclared_variables(template_ats)

            return required_context
        else:
            raise Exception("Template Not Found")


if __name__ == "__main__":
    # render_latex_pdf()
    required_context_set = get_required_context()
    print(required_context_set)
