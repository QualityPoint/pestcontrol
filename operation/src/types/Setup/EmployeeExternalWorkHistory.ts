
export interface EmployeeExternalWorkHistory{
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
	/**	Company : Data	*/
	company_name?: string
	/**	Designation : Data	*/
	designation?: string
	/**	Salary : Currency	*/
	salary?: number
	/**	Address : Small Text	*/
	address?: string
	/**	Contact : Data	*/
	contact?: string
	/**	Total Experience : Data	*/
	total_experience?: string
}