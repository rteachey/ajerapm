import requests
from typing import Literal, ClassVar
from pydantic import BaseModel, Field, ConfigDict
from .authentication import _API, _PW, _USER
from .errors import AjeraError


# Ajera API bits
_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
_CREATE_API_SESSION = "CreateAPISession"
_END_API_SESSION = "EndAPISession"
_LIST_PROJECTS = "ListProjects"
_GET_PROJECTS = "GetProjects"


class AjeraBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Employee(AjeraBaseModel):
    key: int = Field(alias="EmployeeKey")  # example:4262,
    first_name: str = Field(alias="FirstName")  # example:"Mitchell",
    middle_name: str = Field(alias="MiddleName")  # example:"T.",
    last_name: str = Field(alias="LastName")  # example:"Hardert"


class CustomFields(AjeraBaseModel):
    """Customized fields for KBJW projects."""

    proposal_number: str = Field(alias="ProposalNumber")  # example:""
    proposal_date: str | None = Field(alias="ProposalDate")  # example:"2023-09-19"
    created_date: str | None = Field(alias="CreatedDate")  # example:"2023-09-20"
    marketing_source: str = Field(alias="MarketingSource")  # example:""
    non_disclosure_contact: bool = Field(alias="NonDisclosureContact")  # example:false
    po: str = Field(alias="PO")  # example:""
    old_po: str = Field(alias="OLDPO")  # example:""
    header: str = Field(alias="Header")  # example:""
    work_priority: bool = Field(alias="WorkPriority")  # example:0.0
    project_construction_costs: bool = Field(
        alias="ProjectConstructionCosts"
    )  # example:0.0
    construction_cost_change_order: bool = Field(
        alias="ConstructionCostChangeOrder"
    )  # example:0.0
    billing_comment: str = Field(alias="BillingComment")  # example:""
    contract_date: str | None = Field(alias="ContractDate")  # example:"None"
    tm_estimate: float = Field(alias="TMEstimate1")  # example:0.0
    current_submittal_number: float = Field(
        alias="CurrentSubmittalNumber"
    )  # example:0.0
    next_delivery_date: str | None = Field(alias="NextDeliveryDate")  # example:"None"
    project_notes: str = Field(alias="ProjectNotes")  # example:""
    projected_billing_date: str | None = Field(
        alias="ProjectedBillingDate"
    )  # example:"None"
    projected_billing_amount: float | None = Field(
        alias="ProjectedBillingAmount"
    )  # example:0.0

    class WorkStatus(AjeraBaseModel):
        _valid_values = (
            "Active Design",
            "Active Design - Submitted",
            "Active Project",
            "Approved Construction Plans",
        )

        value: Literal[_valid_values] = Field(alias="Value")  # example:"Active Design"
        allow_edit: bool = Field(alias="AllowEdit")  # example:false
        values: tuple[tuple(Literal[v] for v in _valid_values)] = Field(alias="Values")

    work_status: WorkStatus = Field(alias="WorkStatus")


class ProjectInfo(AjeraBaseModel):
    """Return record type for the ListProjects function."""

    key: int = Field(alias="ProjectKey")
    id: str = Field(alias="ID")
    description: str = Field(alias="Description")


class ProjectData(AjeraBaseModel):
    project_key: int = Field(alias="ProjectKey")  # example: 166778
    last_modified_date: str = Field(
        alias="LastModifiedDate"
    )  # example: "2023-09-27 09:57:49.607 GMT-04:00 (Eastern Daylight Time)"
    id: str = Field(alias="ID")  # example: "23-28222-001"
    description: str = Field(
        alias="Description"
    )  # example: "120\" RSC160 Vertical Wet Wells, Infra Pipe Solutions, Logansport, IN"
    sync_to_crm: bool = Field(alias="SyncToCRM")  # example: false
    create_in_crm: bool = Field(alias="CreateInCRM")  # example: false
    crm_final_sync: bool = Field(alias="CRMFinalSync")  # example: false
    status: str = Field(alias="Status")  # example: "Active"
    summarize_billing_group: bool = Field(
        alias="SummarizeBillingGroup"
    )  # example: false
    billing_description: str = Field(alias="BillingDescription")  # example: ""
    company_key: int = Field(alias="CompanyKey")  # example: 1
    company_description: str = Field(
        alias="CompanyDescription"
    )  # example: "Koontz Bryant Johnson Williams, Inc."
    project_type_key: int = Field(alias="ProjectTypeKey")  # example: 5
    project_type_description: str = Field(
        alias="ProjectTypeDescription"
    )  # example: "Industrial"
    department_key: int = Field(alias="DepartmentKey")  # example: 26
    department_description: str = Field(
        alias="DepartmentDescription"
    )  # example: "DOH-Geotechnical"
    budgeted_overhead_rate: float = Field(alias="BudgetedOverheadRate")  # example: 0.0
    project_manager: Employee = Field(alias="ProjectManager")
    principal_in_charge: Employee = Field(alias="PrincipalInCharge")
    marketing_contact: Employee = Field(alias="MarketingContact")
    location: str = Field(alias="Location")  # example: "IN, Logansport"
    wage_table_description: str = Field(alias="WageTableDescription")  # example: ""
    is_certified: bool = Field(alias="IsCertified")  # example: false
    restrict_time_entry_to_resources_only: bool = Field(
        alias="RestrictTimeEntryToResourcesOnly"
    )  # example: false
    tax_state: str = Field(alias="TaxState")  # example: "na"
    tax_local_description: str = Field(alias="TaxLocalDescription")  # example: ""
    # actual_start_date: str|None = Field(alias="ActualStartDate")  # example: "2023-09-20"
    apply_sales_tax: bool = Field(alias="ApplySalesTax")  # example: false
    sales_tax_code: str = Field(alias="SalesTaxCode")  # example: ""
    sales_tax_rate: float = Field(alias="SalesTaxRate")  # example: 0.0
    require_timesheet_notes: bool = Field(
        alias="RequireTimesheetNotes"
    )  # example: true
    notes: str = Field(alias="Notes")  # example: "MST/MTH"
    hours_cost_budget: float = Field(alias="HoursCostBudget")  # example: 0.0
    labor_cost_budget: float = Field(alias="LaborCostBudget")  # example: 0.0
    expense_cost_budget: float = Field(alias="ExpenseCostBudget")  # example: 0.0
    consultant_cost_budget: float = Field(alias="ConsultantCostBudget")  # example: 0.0
    percent_distribution: float = Field(alias="PercentDistribution")  # example: 0.0
    is_final_budget: bool = Field(alias="IsFinalBudget")  # example: false
    billing_type: str = Field(alias="BillingType")  # example: "FixedFee"
    rate_table_key: int = Field(alias="RateTableKey")  # example: 1
    rate_table_description: str = Field(
        alias="RateTableDescription"
    )  # example: "KBJW - Standard Billing Rates"
    total_contract_amount: float = Field(
        alias="TotalContractAmount"
    )  # example: 30000.0
    labor_contract_amount: float = Field(
        alias="LaborContractAmount"
    )  # example: 30000.0
    expense_contract_amount: float = Field(
        alias="ExpenseContractAmount"
    )  # example: 0.0
    consultant_contract_amount: float = Field(
        alias="ConsultantContractAmount"
    )  # example: 0.0
    bill_labor_as_te: bool = Field(alias="BillLaborAsTE")  # example: false
    bill_expense_as_te: bool = Field(alias="BillExpenseAsTE")  # example: true
    bill_consultant_as_te: bool = Field(alias="BillConsultantAsTE")  # example: false
    lock_fee: bool = Field(alias="LockFee")  # example: false
    construction_cost: float = Field(alias="ConstructionCost")  # example: 0.0
    percent_of_construction_cost: float = Field(
        alias="PercentOfConstructionCost"
    )  # example: 0.0
    labor_entry: bool = Field(alias="LaborEntry")  # example: true
    expense_consultant_entry: bool = Field(
        alias="ExpenseConsultantEntry"
    )  # example: true
    custom_fields: CustomFields = Field(alias="CustomFields")


class Phase(AjeraBaseModel):
    """Return record type for the GetProjects function."""

    project_key: int = Field(alias="ProjectKey")  # example:166778
    phase_key: int = Field(alias="PhaseKey")  # example:166779
    parent_key: int = Field(alias="ParentKey")  # example:166778
    invoice_group_key: int = Field(alias="InvoiceGroupKey")  # example:49536
    last_modified_date: str = Field(
        alias="LastModifiedDate"
    )  # example::"2023-09-27 09:57:49.607 GMT-04:00 (Eastern Daylight Time)"
    id: str = Field(alias="ID")  # example:"100"
    description: str = Field(alias="Description")  # example:"Peer Review"
    sync_to_crm: bool = Field(alias="SyncToCRM")  # example:false
    create_in_crm: bool = Field(alias="CreateInCRM")  # example:false
    crm_final_sync: bool = Field(alias="CRMFinalSync")  # example:false
    status: str = Field(alias="Status")  # example:"Active"
    is_billing_group: bool = Field(alias="IsBillingGroup")  # example:false
    summarize_billing_group: bool = Field(
        alias="SummarizeBillingGroup"
    )  # example:false
    billing_description: str = Field(
        alias="BillingDescription"
    )  # example:"Peer Review"
    consultant_invoice_text: str = Field(alias="ConsultantInvoiceText")  # example:""
    expense_invoice_text: str = Field(alias="ExpenseInvoiceText")  # example:""
    labor_invoice_text: str = Field(alias="LaborInvoiceText")  # example:""
    phase_invoice_text: str = Field(alias="PhaseInvoiceText")  # example:""
    project_type_key: int = Field(alias="ProjectTypeKey")  # example:5
    project_type_description: str = Field(
        alias="ProjectTypeDescription"
    )  # example:"Industrial"
    department_key: int = Field(alias="DepartmentKey")  # example:26
    department_description: str = Field(
        alias="DepartmentDescription"
    )  # example:"DOH-Geotechnical"
    budgeted_overhead_rate: float = Field(alias="BudgetedOverheadRate")  # example:0.0
    project_manager: Employee = Field(alias="ProjectManager")
    principal_in_charge: Employee = Field(alias="PrincipalInCharge")
    marketing_contact: Employee = Field(alias="MarketingContact")
    wage_table_description: str = Field(alias="WageTableDescription")  # example:""
    is_certified: bool = Field(alias="IsCertified")  # example:false
    restrict_time_entry_to_resources_only: bool = Field(
        alias="RestrictTimeEntryToResourcesOnly"
    )  # example:false
    tax_state: str = Field(alias="TaxState")  # example:"na"
    tax_local_description: str = Field(alias="TaxLocalDescription")  # example:""
    # actual_start_date: str|None = Field(alias="ActualStartDate")  # example:"2023-09-20"
    apply_sales_tax: bool = Field(alias="ApplySalesTax")  # example:false
    sales_tax_code: str = Field(alias="SalesTaxCode")  # example:""
    sales_tax_rate: bool = Field(alias="SalesTaxRate")  # example:0.0
    require_timesheet_notes: bool = Field(alias="RequireTimesheetNotes")  # example:true
    notes: str = Field(alias="Notes")  # example:"MST/MTH"
    hours_cost_budget: float = Field(alias="HoursCostBudget")  # example:0.0
    labor_cost_budget: float = Field(alias="LaborCostBudget")  # example:0.0
    expense_cost_budget: float = Field(alias="ExpenseCostBudget")  # example:0.0
    consultant_cost_budget: float = Field(alias="ConsultantCostBudget")  # example:0.0
    percent_distribution: float = Field(alias="PercentDistribution")  # example:0.0
    is_final_budget: bool = Field(alias="IsFinalBudget")  # example:false
    billing_type: str = Field(alias="BillingType")  # example:"FixedFee"
    rate_table_key: int = Field(alias="RateTableKey")  # example:1
    rate_table_description: str = Field(
        alias="RateTableDescription"
    )  # example:"KBJW - Standard Billing Rates"
    total_contract_amount: float = Field(alias="TotalContractAmount")  # example:30000.0
    labor_contract_amount: float = Field(alias="LaborContractAmount")  # example:30000.0
    expense_contract_amount: float = Field(alias="ExpenseContractAmount")  # example:0.0
    consultant_contract_amount: float = Field(
        alias="ConsultantContractAmount"
    )  # example:0.0
    bill_labor_as_te: bool = Field(alias="BillLaborAsTE")  # example:false
    bill_expense_as_te: bool = Field(alias="BillExpenseAsTE")  # example:true
    bill_consultant_as_te: bool = Field(alias="BillConsultantAsTE")  # example:false
    lock_fee: bool = Field(alias="LockFee")  # example:false
    labor_entry: bool = Field(alias="LaborEntry")  # example:true
    expense_consultant_entry: bool = Field(
        alias="ExpenseConsultantEntry"
    )  # example:true
    custom_fields: CustomFields = Field(alias="CustomFields")


class InvoiceGroup(AjeraBaseModel):
    invoice_group_key: int = Field(alias="InvoiceGroupKey")  # example: 49536
    project_key: int = Field(alias="ProjectKey")  # example: 166778
    description: str = Field(alias="Description")  # example: "Invoice Group"
    client_key: int = Field(alias="ClientKey")  # example: 4429
    client_description: str = Field(
        alias="ClientDescription"
    )  # example: "Infra Pipe Solutions"
    invoice_format_key: int = Field(alias="InvoiceFormatKey")  # example: 30
    invoice_format_description: str = Field(
        alias="InvoiceFormatDescription"
    )  # example: "Fixed Fee - New Format - 7/2017"
    email_invoice_template_key: int = Field(
        alias="EmailInvoiceTemplateKey"
    )  # example: 1
    email_invoice_template_description: str = Field(
        alias="EmailInvoiceTemplateDescription"
    )  # example: "Default Template"
    email_client_statement_template_description: str = Field(
        alias="EmailClientStatementTemplateDescription"
    )  # example: ""
    print_backup: bool = Field(alias="PrintBackup")  # example: false
    email_include_backup: bool = Field(alias="EmailIncludeBackup")  # example: false
    billing_manager: Employee = Field(alias="BillingManager")  # example
    invoice_header_text: str = Field(
        alias="InvoiceHeaderText"
    )  # example: "Professional Services"
    invoice_footer_text: str = Field(
        alias="InvoiceFooterText"
    )  # example: "Terms:  Net 30 "
    invoice_scope: str = Field(alias="InvoiceScope")  # example: ""
    notes: str = Field(alias="Notes")  # example: ""


class Content(AjeraBaseModel):
    pass


class CreateSessionContent(Content):
    company_name: str = Field(
        alias="CompanyName"
    )  # example: "Koontz Bryant Johnson Williams, INC."
    using_icr_mobile: bool = Field(alias="UsingICRMobile")  # example: true
    session_token: str = Field(alias="SessionToken")  # example: ""
    session_expiration: str = Field(
        alias="SessionExpiration"
    )  # example: "2023-10-08T13:20:48.3275167-04:00"
    api_url: str = Field(alias="APIURL")
    ajera_version: str = Field(alias="AjeraVersion")  # example: "9.90.02"

    class ICRConfigFile(AjeraBaseModel):
        icr_url: str = Field(alias="icrURL")  # example: "deltek",
        icr_client_id: str = Field(
            alias="icrClientId"
        )  # example: "vrfNVrWoI8I4IRgswO1b5LVEBuiz3Ra3uljnKVg",
        icr_user_name: str = Field(alias="icrUserName")  # example: "deltek.ajera",
        icr_api_key: str = Field(
            alias="icrApiKey"
        )  # example: "dcb548ba226b6d39bd75daf455ab5005",

    icr_config_file: ICRConfigFile = Field(alias="ICRConfigFile")


class EndSessionContent(Content):
    pass


class ListProjectsContent(Content):
    projects: list[ProjectInfo] = Field(alias="Projects")


class GetProjectsContent(Content):
    projects: list[ProjectData] = Field(alias="Projects")
    invoice_groups: list[InvoiceGroup] = Field(alias="InvoiceGroups")
    phases: list[Phase] = Field(alias="Phases")


class AjeraMethodArguments(AjeraBaseModel):
    # AjeraMethodArguments is an abstract type!!!!
    pass


class ListProjectsArgs(AjeraMethodArguments):
    by_status: list | None = Field(
        alias="FilterByStatus"
    )  # example: ["Preliminary", "Hold"]
    by_company: list | None = Field(alias="FilterByCompany")  # example =[1]
    by_name_like: str | None = Field(
        alias="FilterByNameLike"
    )  # example = "Description"
    by_description_like: str | None = Field(
        alias="FilterByDescriptionLike"
    )  # example = "Project Description"
    by_description_equals: str | None = Field(
        alias="FilterByDescriptionEquals"
    )  # example = "Project Description"
    by_id_like: str | None = Field(alias="FilterByIDLike")  # example = "20772"
    by_project_type: list | None = Field(
        alias="FilterByProjectType"
    )  # example = [1, null]
    by_sync_to_crm: list[bool] | None = Field(
        alias="FilterBySyncToCRM"
    )  # example = [true]
    by_earliest_modified_date: str | None = Field(
        alias="FilterByEarliestModifiedDate"
    )  # example = "2023-03-11"
    by_latest_modified_date: str | None = Field(
        alias="FilterByLatestModifiedDate"
    )  # example: "2023-03-11"


class GetProjectsArgs(AjeraMethodArguments):
    requested_projects: list[int] = Field(
        alias="RequestedProjects"
    )  # example: [1, 2, 3]


class AjeraResponse(AjeraBaseModel):
    response_code: int = Field(alias="ResponseCode")  # example: 200
    message: str = Field(alias="Message")  # example: "Success"
    errors: list = Field(alias="Errors")  # example: []
    content: CreateSessionContent | EndSessionContent | ListProjectsContent | GetProjectsContent = Field(
        alias="Content"
    )
    usage_key: str = Field(
        alias="UsageKey"
    )  # example: "ad3d4b0e-0279-4778-b03c-a3127c8a3ef9"


class CreateSessionResponse(AjeraResponse):
    content: CreateSessionContent = Field(alias="Content")


class EndSessionResponse(AjeraResponse):
    content: EndSessionContent = Field(alias="Content")


class ListProjectsResponse(AjeraResponse):
    content: ListProjectsContent = Field(alias="Content")


class GetProjectsResponse(AjeraResponse):
    content: GetProjectsContent = Field(alias="Content")


class AjeraRequest(AjeraBaseModel):
    response_type: ClassVar
    method: str = Field(alias="Method")

    def post(self):
        requests_resp = requests.post(
            url=_API,
            headers=_HEADERS,
            json=self.model_dump(mode="json", by_alias=True, exclude_none=True),
        )
        requests_resp_json = requests_resp.json()
        if requests_resp_json["Errors"]:
            raise AjeraError(self)
        ajera_resp = self.response_type.model_validate(requests_resp_json)
        return ajera_resp


class CreateSession(AjeraRequest):
    response_type = CreateSessionResponse
    method: Literal[_CREATE_API_SESSION] = Field(
        alias="Method", default=_CREATE_API_SESSION
    )
    username: Literal[_USER] = Field(
        alias="Username", default=_USER
    )  # example:"janedoe"
    password: Literal[_PW] = Field(alias="Password", default=_PW)  # example:"j@ned0e"
    api_version: Literal[2] = Field(alias="APIVersion", default=2)  # 1 or 2
    use_session_cookie: bool = Field(
        alias="UseSessionCookie", default=False
    )  # example:false


class EndSession(AjeraRequest):
    response_type = EndSessionResponse
    method: Literal[_END_API_SESSION] = Field(alias="Method", default=_END_API_SESSION)
    session_token: str = Field(alias="SessionToken")


class AjeraCall(AjeraRequest):
    args_type: ClassVar
    session_token: str = Field(alias="SessionToken")
    method_arguments: AjeraMethodArguments = Field(alias="MethodArguments")


class ListProjects(AjeraCall):
    args_type = ListProjectsArgs
    response_type = ListProjectsResponse
    method: Literal[_LIST_PROJECTS] = Field(alias="Method", default=_LIST_PROJECTS)
    method_arguments: ListProjectsArgs = Field(alias="MethodArguments")


class GetProjects(AjeraCall):
    args_type = GetProjectsArgs
    response_type = GetProjectsResponse
    method: Literal[_GET_PROJECTS] = Field(alias="Method", default=_GET_PROJECTS)
    method_arguments: GetProjectsArgs = Field(alias="MethodArguments")
