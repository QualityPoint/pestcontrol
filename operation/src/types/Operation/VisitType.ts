
export interface VisitType{
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
	/**	Visit Type : Data	*/
	visit_type: string
	/**	Description : Small Text	*/
	description?: string
}