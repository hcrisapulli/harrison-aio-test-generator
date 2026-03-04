"""
templates_db.py
Building block library for AIO test case generation.
Derived from real SmartDocs test suites.
"""

# ---------------------------------------------------------------------------
# COVERAGE CATEGORIES — used for the checklist questions
# ---------------------------------------------------------------------------

COVERAGE_CATEGORIES = {
    "crud": {
        "label": "Does this feature involve creating, editing, or deleting items?",
        "short": "CRUD operations",
    },
    "list_view": {
        "label": "Does this feature have a list or table view?",
        "short": "List / table view",
    },
    "form_validation": {
        "label": "Does this feature have a form with required fields?",
        "short": "Form validation",
    },
    "permissions": {
        "label": "Does this feature have permission or role restrictions?",
        "short": "Permissions / access control",
    },
    "integration": {
        "label": "Does this feature connect to an external system (Xero, QuickBooks)?",
        "short": "External integration",
    },
    "export": {
        "label": "Does this feature involve exporting or downloading files?",
        "short": "Export / download",
    },
    "status_transition": {
        "label": "Does this feature involve document or item status changes?",
        "short": "Status transitions",
    },
    "wizard": {
        "label": "Does this feature use a multi-step wizard or flow?",
        "short": "Multi-step wizard",
    },
    "conditional_logic": {
        "label": "Does the feature behave differently depending on a condition or setting?",
        "short": "Conditional logic",
    },
    "error_handling": {
        "label": "Can this feature produce errors or empty/edge-case states?",
        "short": "Error handling / edge cases",
    },
}

# ---------------------------------------------------------------------------
# FEATURE TEMPLATES
# Each entry: title, precondition, steps[], results[], priority, tags
# Placeholders use {module}, {item}, {items}, {document_type}, {integration},
# {status}, {filter_type}, {field}, {action}, {condition}, {wizard_name}
# ---------------------------------------------------------------------------

FEATURE_TEMPLATES = {

    # ── Export ────────────────────────────────────────────────────────────────
    "export": [
        {
            "title": "Export_Verify export option is available from the {location}",
            "precondition": "{document_type} document exists in entity",
            "priority": "High",
            "tags": "Export",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a {document_type} document",
                "Open the {location}",
            ],
            "results": [
                "User should be successfully navigated to the Documents page",
                "{document_type} document should be selected",
                "Export option should be visible in the {location}",
            ],
        },
        {
            "title": "Export_Verify file type selector displays correct options",
            "precondition": "{document_type} document exists in entity",
            "priority": "High",
            "tags": "Export",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a {document_type} document",
                "Select Export from the options",
                "Check the available file type options",
            ],
            "results": [
                "Export dialog should open",
                "File type selector should display the correct options",
            ],
        },
        {
            "title": "Export_Verify exported file downloads successfully",
            "precondition": "{document_type} document exists in entity",
            "priority": "Critical",
            "tags": "Export",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a {document_type} document",
                "Select Export from the options",
                "Select the desired file type",
                "Click the Export button to download the file",
            ],
            "results": [
                "Export dialog should open",
                "File should download successfully",
                "Downloaded file should be valid and contain correct data",
            ],
        },
        {
            "title": "Export_Verify Xero Conversion Toolbox link displays for CSV export",
            "precondition": "{document_type} document exists in entity",
            "priority": "High",
            "tags": "Export,Xero",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a {document_type} document",
                "Select Export from the options",
                "Change the export file type to CSV",
                "Change the format to 'Xero Conversion Toolbox'",
            ],
            "results": [
                "Export dialog should open",
                "CSV file type should be selected",
                "Xero Conversion Toolbox link should display under the format selector",
            ],
        },
        {
            "title": "Export_Verify Xero Conversion Toolbox link does not display for non-CSV file types",
            "precondition": "{document_type} document exists in entity",
            "priority": "Medium",
            "tags": "Export,Xero",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a {document_type} document",
                "Select Export from the options",
                "Change the export file type to a non-CSV option (e.g. PDF or Excel)",
            ],
            "results": [
                "Export dialog should open",
                "Non-CSV file type should be selected",
                "Xero Conversion Toolbox link should not display",
            ],
        },
    ],

    # ── CRUD (generic) ────────────────────────────────────────────────────────
    "crud": [
        {
            "title": "{module}_Verify the loading of the {item} list",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Verify the loading of the {item} list",
            ],
            "results": [
                "User should be successfully navigated to the {module} page",
                "The {item} list should load successfully",
                "The first 50 {items} should load",
            ],
        },
        {
            "title": "{module}_Create a {item}",
            "precondition": "",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button",
                "Fill in all required fields and click 'Create {item}'",
            ],
            "results": [
                "User should be successfully navigated to the {module} page",
                "'+ New {item}' button should be visible",
                "Create {item} dialog should open",
                "New {item} should be saved and appear in the {item} list",
            ],
        },
        {
            "title": "{module}_Edit a {item}",
            "precondition": "{item} exists in the {module} list",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the edit icon for the {item}",
                "Make changes to the fields and click Save",
            ],
            "results": [
                "Edit dialog should open with the existing {item} details",
                "Fields should be editable",
                "Changes should be saved and reflected in the {item} list",
            ],
        },
        {
            "title": "{module}_Delete a {item}",
            "precondition": "{item} exists in the {module} list",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the 3-dot action button for the {item}",
                "Click the Delete option",
                "Confirm the deletion",
            ],
            "results": [
                "3-dot action menu should show the Delete option",
                "A confirmation dialog should display",
                "{item} should be removed from the {item} list",
                "The {item} count should update to reflect the current number",
            ],
        },
    ],

    # ── List / filter ─────────────────────────────────────────────────────────
    "list_view": [
        {
            "title": "{module}_Verify {item} list loads with lazy pagination",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Scroll down past the first 50 {items}",
            ],
            "results": [
                "The first 50 {items} should load",
                "Lazy loading should apply — the next 50 {items} should load on scroll",
            ],
        },
        {
            "title": "{module}_Verify {item} list filter applies correctly",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Apply a {filter_type} filter",
            ],
            "results": [
                "The {item} list should update to show only matching {items}",
                "The filter should be applied correctly",
            ],
        },
    ],

    # ── Form validation ───────────────────────────────────────────────────────
    "form_validation": [
        {
            "title": "{module}_Verify required fields are enforced when creating a {item}",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button",
                "Leave required fields blank and click Save",
            ],
            "results": [
                "A meaningful error message should display for each missing required field",
                "The {item} should not be saved",
            ],
        },
        {
            "title": "{module}_Verify optional fields can be left blank",
            "precondition": "",
            "priority": "Low",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button",
                "Fill in only the required fields and click Save",
            ],
            "results": [
                "The {item} should be saved successfully without optional fields",
                "Optional fields should be left blank",
            ],
        },
    ],

    # ── Connections / Integration ──────────────────────────────────────────────
    "connections": [
        {
            "title": "Connections_Link entity to {integration}",
            "precondition": "Non-integrated entity selected",
            "priority": "High",
            "tags": "Connections,{integration}",
            "steps": [
                "Login to SmartDocs",
                "Select a non-integrated entity",
                "Navigate to the Connections page",
                "Click the '+ Setup' button for the {integration} option",
                "Complete the connection setup",
            ],
            "results": [
                "User should be successfully navigated to the Connections page",
                "{integration} setup option should be visible",
                "Connection setup should complete successfully",
                "{integration} should show as connected with the organisation name and connection date",
                "Entity should show with an integration badge",
            ],
        },
        {
            "title": "Connections_Disconnect entity from {integration}",
            "precondition": "Entity is connected to {integration}",
            "priority": "High",
            "tags": "Connections,{integration}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity connected to {integration}",
                "Navigate to the Connections page",
                "Click the Disconnect button for {integration}",
                "Confirm the disconnection",
            ],
            "results": [
                "A confirmation dialog should display",
                "{integration} should no longer show as connected",
                "The integration badge should not show for the entity",
            ],
        },
        {
            "title": "Connections_Verify active connection details display correctly",
            "precondition": "Entity is connected to {integration}",
            "priority": "Medium",
            "tags": "Connections,{integration}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity connected to {integration}",
                "Navigate to the Connections page",
                "Verify the {integration} connection details",
            ],
            "results": [
                "Organisation name should display",
                "Connection date should display",
                "Open in {integration} link should be visible and functional",
            ],
        },
    ],

    # ── Integration badge ─────────────────────────────────────────────────────
    "integration": [
        {
            "title": "{module}_Verify integration badge displays for synced {item}",
            "precondition": "Entity is connected to {integration}",
            "priority": "Medium",
            "tags": "{module},{integration}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity connected to {integration}",
                "Navigate to the {module} page",
                "Create or sync a {item} with {integration}",
            ],
            "results": [
                "{item} should show with an integration badge",
                "The badge should indicate the {integration} connection",
            ],
        },
        {
            "title": "{module}_Verify {item} syncs to {integration}",
            "precondition": "Entity is connected to {integration}",
            "priority": "High",
            "tags": "{module},{integration}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity connected to {integration}",
                "Navigate to the {module} page",
                "Create a {item} and enable syncing",
            ],
            "results": [
                "{item} should be synced to {integration} successfully",
                "Last Synced date should update",
                "Integration badge should display on the {item}",
            ],
        },
    ],

    # ── AP Workflow ────────────────────────────────────────────────────────────
    "ap_workflow": [
        {
            "title": "AP_Verify Payment Method auto-selection when document becomes Awaiting Payment",
            "precondition": "Entity has a Supplier contact with Preferred Payment Method set. No AP Workflow Payment Method configured.",
            "priority": "Critical",
            "tags": "AP,Payment Method",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a document and update the status to 'Awaiting Payment'",
            ],
            "results": [
                "Payment Method field should be auto-populated with the Supplier contact's Preferred Payment Method",
                "Pay To details should be prefilled if available",
            ],
        },
        {
            "title": "AP_Verify AP Workflow Payment Method takes priority over Supplier contact method",
            "precondition": "AP Workflow has a Payment Method configured. Supplier contact also has a Preferred Payment Method set.",
            "priority": "Critical",
            "tags": "AP,Payment Method,AP Workflow",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a document and update the status to 'Awaiting Payment'",
            ],
            "results": [
                "Payment Method should be auto-populated with the AP Workflow Payment Method",
                "AP Workflow Payment Method should take priority over the Supplier contact's Preferred Payment Method",
            ],
        },
        {
            "title": "AP_Verify Payment Method dropdown options",
            "precondition": "",
            "priority": "High",
            "tags": "AP,Payment Method",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the AP screen",
                "Click on the Payment Method dropdown",
            ],
            "results": [
                "Payment Method dropdown should display the following options: Cash, Credit Card, Direct Debit, ABA, BPAY, Cheque, Bank Transfer",
            ],
        },
        {
            "title": "AP_Verify Pay To details are extracted from document when available",
            "precondition": "Document contains extractable payment details",
            "priority": "High",
            "tags": "AP,Payment Method",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Upload a document which contains payment details",
                "Update the document status to 'Awaiting Payment'",
            ],
            "results": [
                "Pay To details should be extracted from the document and prefilled",
                "Bank Account Name, BSB, and Account Number should be populated if present in the document",
            ],
        },
        {
            "title": "AP_Verify Pay To details are left blank when document has no payment details",
            "precondition": "Document does not contain extractable payment details. Supplier contact has no Financial Details filled.",
            "priority": "Medium",
            "tags": "AP,Payment Method",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Upload a document with no payment details",
                "Update the document status to 'Awaiting Payment'",
            ],
            "results": [
                "Pay To fields should be left blank for manual input",
            ],
        },
    ],

    # ── Status transitions ─────────────────────────────────────────────────────
    "status_transition": [
        {
            "title": "{module}_Verify document status can be changed to '{status}'",
            "precondition": "Document exists in entity",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a document",
                "Update the document status to '{status}'",
            ],
            "results": [
                "Document status should update to '{status}' successfully",
                "Status change should be reflected in the document list",
            ],
        },
        {
            "title": "{module}_Verify behaviour triggered when document status changes to '{status}'",
            "precondition": "Document exists in entity",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Select a document",
                "Update the document status to '{status}'",
                "Verify the triggered behaviour",
            ],
            "results": [
                "Status should update to '{status}'",
                "Expected behaviour should trigger automatically on status change",
            ],
        },
    ],

    # ── Wizard ─────────────────────────────────────────────────────────────────
    "wizard": [
        {
            "title": "{module}_Verify {wizard_name} wizard completes successfully",
            "precondition": "",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button to open the wizard",
                "Complete all steps through the wizard",
                "Click Finish or Create on the final step",
            ],
            "results": [
                "{wizard_name} wizard should open",
                "Each step should progress correctly after clicking Next",
                "Wizard should complete successfully",
                "New {item} should appear in the {module} list",
            ],
        },
        {
            "title": "{module}_Verify {wizard_name} wizard Back button retains data",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button to open the wizard",
                "Complete Step 1 and click Next",
                "Click Back on Step 2",
            ],
            "results": [
                "User should be taken back to Step 1",
                "Previously entered data should be retained",
            ],
        },
        {
            "title": "{module}_Verify {wizard_name} wizard validates required fields before progressing",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button to open the wizard",
                "Leave required fields blank on Step 1 and click Next",
            ],
            "results": [
                "A meaningful error message should display for each required field",
                "Wizard should not progress to the next step until required fields are filled",
            ],
        },
    ],

    # ── Permissions ────────────────────────────────────────────────────────────
    "permissions": [
        {
            "title": "{module}_Verify {item} cannot be deleted when {condition}",
            "precondition": "{condition}",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the 3-dot action button for the {item} that is {condition}",
            ],
            "results": [
                "The Delete option should not be available",
                "{item} should not be able to be deleted when {condition}",
            ],
        },
        {
            "title": "{module}_Verify restricted actions are greyed out when {condition}",
            "precondition": "{condition}",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Attempt to perform a restricted action on the {item} ({condition})",
            ],
            "results": [
                "The restricted action should be greyed out or unavailable",
                "A meaningful message should display explaining the restriction",
            ],
        },
    ],

    # ── Conditional logic ──────────────────────────────────────────────────────
    "conditional_logic": [
        {
            "title": "{module}_Verify {item} behaves correctly when condition is met",
            "precondition": "Relevant condition is configured",
            "priority": "High",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity with the relevant condition configured",
                "Navigate to the {module} page",
                "Trigger the condition",
            ],
            "results": [
                "Expected behaviour should occur when the condition is met",
                "Relevant fields or options should display as expected",
            ],
        },
        {
            "title": "{module}_Verify {item} behaves correctly when condition is not met",
            "precondition": "Relevant condition is not configured",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity without the relevant condition configured",
                "Navigate to the {module} page",
                "Verify the default behaviour",
            ],
            "results": [
                "Default behaviour should apply when the condition is not met",
                "No unexpected fields or options should display",
            ],
        },
    ],

    # ── Error handling ─────────────────────────────────────────────────────────
    "error_handling": [
        {
            "title": "{module}_Verify error message displays when required fields are missing",
            "precondition": "",
            "priority": "Medium",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the {module} page",
                "Click the '+ New {item}' button",
                "Leave required fields blank and click Save",
            ],
            "results": [
                "A meaningful error message should display for each missing required field",
                "The {item} should not be saved",
            ],
        },
        {
            "title": "{module}_Verify empty state displays when no {items} exist",
            "precondition": "No {items} exist in the entity",
            "priority": "Low",
            "tags": "{module}",
            "steps": [
                "Login to SmartDocs",
                "Select an entity with no {items}",
                "Navigate to the {module} page",
            ],
            "results": [
                "An empty state message should display",
                "The {item} count should show as 0",
            ],
        },
    ],

    # ── Bank Statement ─────────────────────────────────────────────────────────
    "bank_statement": [
        {
            "title": "Bank Statement_Verify Switch Dr/Cr button is visible",
            "precondition": "Bank Statement document exists in entity",
            "priority": "High",
            "tags": "Bank Statement,Line Items",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Open a Bank Statement document",
            ],
            "results": [
                "Bank Statement document should open",
                "Switch Dr/Cr button should be visible in the line items section",
            ],
        },
        {
            "title": "Bank Statement_Verify Switch Dr/Cr swaps debit and credit values",
            "precondition": "Bank Statement document exists in entity",
            "priority": "High",
            "tags": "Bank Statement,Line Items",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Open a Bank Statement document",
                "Note the current Dr/Cr values for a transaction",
                "Click the Switch Dr/Cr button",
            ],
            "results": [
                "Debit and credit amounts should swap for all affected transactions",
                "Totals should recalculate to reflect the switched values",
            ],
        },
        {
            "title": "Bank Statement_Verify Switch Dr/Cr only affects applicable transactions",
            "precondition": "Bank Statement document exists in entity with mixed Dr/Cr transactions",
            "priority": "High",
            "tags": "Bank Statement,Line Items",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Open a Bank Statement document",
                "Click the Switch Dr/Cr button for a specific transaction",
            ],
            "results": [
                "Only the selected transaction's Dr/Cr values should be switched",
                "Other transactions should not be affected",
                "Totals should update accordingly",
            ],
        },
    ],

    # ── Document Details / Extraction ──────────────────────────────────────────
    "document_details": [
        {
            "title": "Document Details_Verify {field} is extracted from document",
            "precondition": "Document contains {field} data",
            "priority": "High",
            "tags": "Documents",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Upload a document containing {field} data",
                "Open the document details",
            ],
            "results": [
                "Document should be uploaded successfully",
                "{field} should be read from the document and displayed correctly",
                "{field} value should match the source document",
            ],
        },
        {
            "title": "Document Details_Verify {field} is left blank when not present in document",
            "precondition": "Document does not contain {field} data",
            "priority": "Medium",
            "tags": "Documents",
            "steps": [
                "Login to SmartDocs",
                "Select an entity",
                "Navigate to the Documents page",
                "Upload a document that does not contain {field} data",
                "Open the document details",
            ],
            "results": [
                "Document should be uploaded successfully",
                "{field} should be left blank for manual input",
            ],
        },
    ],

}

# ---------------------------------------------------------------------------
# KEYWORD MAP — maps user input keywords to feature areas
# ---------------------------------------------------------------------------

KEYWORD_MAP = [
    {
        "keywords": ["export", "download", "csv", "excel", "pdf export", "xero export",
                     "file type", "format selector", "conversion toolbox"],
        "features": ["export"],
        "module": "Export", "tags": ["Export"],
    },
    {
        "keywords": ["xero", "xero conversion", "conversion toolbox"],
        "features": ["export", "connections"],
        "module": "Export", "tags": ["Export", "Xero"],
    },
    {
        "keywords": ["ap", "ap workflow", "awaiting payment", "payment method", "pay to",
                     "aba", "bpay", "direct debit", "bank transfer", "cheque", "payment"],
        "features": ["ap_workflow"],
        "module": "AP", "tags": ["AP", "Payment Method"],
    },
    {
        "keywords": ["contact", "contacts", "supplier", "customer", "preferred payment",
                     "financial details", "bsb", "account number"],
        "features": ["crud", "list_view", "permissions"],
        "module": "Contacts", "item": "contact", "tags": ["Contacts"],
    },
    {
        "keywords": ["entit", "entity", "entities", "entity wizard", "business structure",
                     "abn", "entity code", "industry"],
        "features": ["crud", "list_view", "wizard"],
        "module": "Entities", "item": "entity", "tags": ["Entities"],
    },
    {
        "keywords": ["categor", "categories", "category", "category type"],
        "features": ["crud", "list_view"],
        "module": "Categories", "item": "category", "tags": ["Categories"],
    },
    {
        "keywords": ["connection", "connect", "disconnect", "integration", "link entity",
                     "xero connect", "quickbooks", "accounting software"],
        "features": ["connections"],
        "module": "Connections", "tags": ["Connections"],
    },
    {
        "keywords": ["document", "documents", "upload", "model editor", "extraction",
                     "document list", "document details", "invoice", "receipt"],
        "features": ["crud", "list_view", "document_details"],
        "module": "Documents", "item": "document", "tags": ["Documents"],
    },
    {
        "keywords": ["bank statement", "bank", "dr cr", "dr/cr", "switch dr",
                     "debit credit", "transactions"],
        "features": ["bank_statement"],
        "module": "Bank Statement", "tags": ["Bank Statement"],
    },
    {
        "keywords": ["status", "status change", "awaiting", "approved", "rejected",
                     "published", "draft status", "workflow status"],
        "features": ["status_transition"],
        "module": "Documents", "tags": ["Documents"],
    },
    {
        "keywords": ["setting", "settings", "configuration", "configure", "preferences"],
        "features": ["crud"],
        "module": "Settings", "item": "setting", "tags": ["Settings"],
    },
    {
        "keywords": ["permission", "role", "access", "restrict", "admin", "user role"],
        "features": ["permissions"],
        "module": "Permissions", "tags": ["Permissions"],
    },
    {
        "keywords": ["wizard", "multi-step", "multistep", "onboarding", "setup flow"],
        "features": ["wizard"],
        "module": "Wizard", "tags": [],
    },
    {
        "keywords": ["sync", "syncing", "synchronise", "synchronize", "integrate"],
        "features": ["integration"],
        "module": "Connections", "tags": ["Connections"],
    },
    {
        "keywords": ["error", "validation", "required field", "missing", "empty state", "edge case"],
        "features": ["error_handling"],
        "module": "", "tags": [],
    },
]

# Coverage category → template key mapping (for checklist expansion)
CHECKLIST_FEATURE_MAP = {
    "crud":             ["crud"],
    "list_view":        ["list_view"],
    "form_validation":  ["form_validation"],
    "permissions":      ["permissions"],
    "integration":      ["integration", "connections"],
    "export":           ["export"],
    "status_transition":["status_transition"],
    "wizard":           ["wizard"],
    "conditional_logic":["conditional_logic"],
    "error_handling":   ["error_handling"],
}
