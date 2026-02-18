
export interface VisitTimesheet{
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
	/**	From Time : Datetime	*/
	from_time: string
	/**	To Time : Datetime	*/
	to_time: string
	/**	Duration : Time	*/
	duration?: string
}