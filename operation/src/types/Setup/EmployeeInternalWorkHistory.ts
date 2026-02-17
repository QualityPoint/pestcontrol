
export interface EmployeeInternalWorkHistory{
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
	/**	Branch : Link - Branch	*/
	branch?: string
	/**	Department : Link - Department	*/
	department?: string
	/**	Designation : Link - Designation	*/
	designation?: string
	/**	From Date : Date	*/
	from_date?: string
	/**	To Date : Date	*/
	to_date?: string
}