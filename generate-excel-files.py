import os
from converter import json_files_to_excel, yaml_files_to_excel

# merge json files to excel
CMA_FRONTEND_TRANSLATION_DIRECTORY = os.path.expanduser("~/source/cma-frontend/src/assets/i18n")
json_files_to_excel(eng_file=f"{CMA_FRONTEND_TRANSLATION_DIRECTORY}/en.json",
                    vi_file=f"{CMA_FRONTEND_TRANSLATION_DIRECTORY}/vi.json",
                    excel_file="cma-translation.xlsx",
                    sheet_name="cma")
print("json files to excel done")

#merge yaml files to excel
EREC_TRANSLATION_DIRECTORY = os.path.expanduser("~/source/e-recruitment/packages/vietnam/core/translation")
yaml_files_to_excel(eng_file=f"{EREC_TRANSLATION_DIRECTORY}/en.yml",
                    vi_file=f"{EREC_TRANSLATION_DIRECTORY}/vn.yml",
                    excel_file="erec-translation.xlsx",
                    sheet_name="erec")
print("yaml files to excel done")