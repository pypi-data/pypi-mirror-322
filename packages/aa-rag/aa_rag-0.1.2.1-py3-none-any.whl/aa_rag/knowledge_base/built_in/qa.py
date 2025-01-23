# import sqlite3
# from pathlib import Path
#
# from aa_rag import setting
# from aa_rag.knowledge_base.base import BaseKnowledge
#
#
# class QAKnowledge(BaseKnowledge):
#     _knowledge_name = "QA"
#
#     def __init__(self, relation_db_path: str = setting.db.relation.uri, **kwargs):
#         """
#         QA Knowledge Base. Built-in Knowledge Base.
#         Args:
#             relation_db_path: The path of the relation database.
#             **kwargs: The keyword arguments.
#         """
#         super().__init__(**kwargs)
#
#         # create the directory and file if not exist
#         relation_db_path_obj = Path(relation_db_path)
#         if not relation_db_path_obj.exists():
#             relation_db_path_obj.touch()
#         # create the connection and create the table if not exist
#         self.relation_db_conn = sqlite3.connect(relation_db_path)
#         self.relation_table_name = self.knowledge_name.lower()
#         self.relation_db_conn.execute(f"""
#             CREATE TABLE IF NOT EXISTS {self.relation_table_name} (
#                 project_id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 guides TEXT NOT NULL,
#                 project_meta TEXT NOT NULL)""")
#         self.relation_db_conn.commit()
#
#     def _is_compatible_env(
#         self, source_env_info: CompatibleEnv, target_env_info: CompatibleEnv
#     ) -> bool:
#         """
#         Check if the source environment is compatible with the target environment.
#         Args:
#             source_env_info: to be checked
#             target_env_info: to be checked
#
#         Returns:
#             bool: True if compatible, False otherwise.
#         """
#         prompt_template = ChatPromptTemplate.from_messages(
#             [
#                 (
#                     "system",
#                     """You are an expert in computer hardware device information.
#                     I will provide you with two jsons. Each json is the detailed data of a computer hardware device information.
#                     --Requirements--
#                     1. Please determine whether the two devices are compatible. If compatible, please return "True". Otherwise, return "False".
#                     2. Do not return other information. Just return "True" or "False".
#
#                     --Data--
#                     source_env_info: {source_env_info}
#                     target_env_info: {target_env_info}
#
#                     --Result--
#                     result:
#                     """,
#                 )
#             ]
#         )
#         return self._ask(prompt_template, source_env_info, target_env_info)
#
#     def _ask(
#         self, prompt_template: ChatPromptTemplate, source_env_info: CompatibleEnv, target_env_info: CompatibleEnv
#     ) -> bool:
#         """
#         Ask the question.
#         Args:
#             prompt_template: The
