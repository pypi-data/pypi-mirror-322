# Copyright 2024-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Knowledge Pages API",
    "version": "12.0.1.2.1",
    "depends": [
        "base",
        "knowledge",
        "base_rest",
        "document_page",
        "document_page_tag",
        "auth_api_key",
        "knowledge_translatable_pages",
        "api_common_base",
    ],
    "author": """
        Som It Cooperatiu SCCL,
        Som Connexió SCCL,
        Odoo Community Association (OCA)
    """,
    "category": "Knowledge",
    "website": "https://gitlab.com/somitcoop/erp-research/odoo-helpdesk",
    "license": "AGPL-3",
    "summary": """
        REST API for Knowledge Pages
    """,
    "data": [
        "views/knowledge_page_view.xml",
        "views/knowledge_page_highlight.xml",
        "security/ir.model.access.csv",
    ],
    "application": False,
    "installable": True,
}
