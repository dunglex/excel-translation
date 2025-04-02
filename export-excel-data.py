import os
from converter import excel_to_json_files, excel_to_yaml_files

# export excel to json files
CMA_FRONTEND_TRANSLATION_DIRECTORY = os.path.expanduser("~/source/cma-frontend/src/assets/i18n")
excel_to_json_files(excel_file="cma-translation.xlsx",
                    eng_file=f"{CMA_FRONTEND_TRANSLATION_DIRECTORY}/en.json",
                    vi_file=f"{CMA_FRONTEND_TRANSLATION_DIRECTORY}/vi.json")
print("excel to json files done")

# export excel to yaml files
EREC_TRANSLATION_DIRECTORY = os.path.expanduser("~/source/e-recruitment/packages/vietnam/core/translation")
excel_to_yaml_files(excel_file="erec-translation.xlsx",
                    eng_file=f"{EREC_TRANSLATION_DIRECTORY}/en.yml",
                    vi_file=f"{EREC_TRANSLATION_DIRECTORY}/vn.yml")
print("excel to yaml files done")
