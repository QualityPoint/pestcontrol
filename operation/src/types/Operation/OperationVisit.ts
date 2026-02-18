import { VisitTimesheet } from './VisitTimesheet'
import { VisitOperationTeam } from './VisitOperationTeam'

export interface OperationVisit{
	name: string
	creation: string
	modified: string
	owner: string
	modified_by: string
	docstatus: 0 | 1 | 2
	parent?: string
	parentfield?: string
	parenttype?: string
	idx?: number
	/**	Series : Select	*/
	naming_series: "OPR-VST-.YYYY.-"
	/**	Customer : Link - Customer	*/
	customer: string
	/**	Tax ID : Data	*/
	tax_id?: string
	/**	Customer Name : Data	*/
	customer_name?: string
	/**	Project : Link - Project	*/
	project: string
	/**	Visit Date : Data	*/
	visit_date: string
	/**	Visit No : Data	*/
	visit_no: string
	/**	Company : Link - Company	*/
	company: string
	/**	Visit Type : Link - Visit Type	*/
	visit_type: string
	/**	Amended From : Link - Operation Visit	*/
	amended_from?: string
	/**	Timesheet : Table - Visit Timesheet	*/
	timesheet: VisitTimesheet[]
	/**	No of Interval : Int	*/
	no_of_interval?: number
	/**	Visit Duration : Time	*/
	visit_duration?: string
	/**	Visit Timeout : Time	*/
	visit_timeout?: string
	/**	Operation Supervisor : Link - Operation Team Member	*/
	operation_supervisor: string
	/**	Team Members : Table - Visit Operation Team	*/
	team_members: VisitOperationTeam[]
	/**	Visit Address : Link - Address	*/
	visit_address_name?: string
	/**	Visit Address : Small Text	*/
	visit_address?: string
}