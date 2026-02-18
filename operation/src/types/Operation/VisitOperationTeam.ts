
export interface VisitOperationTeam{
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
	/**	Team Member : Link - Operation Team Member	*/
	team_member: string
	/**	Member Name : Data	*/
	member_name?: string
}