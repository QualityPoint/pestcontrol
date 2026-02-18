
export interface OperationTeamMember{
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
	/**	Team Member : Link - Employee	*/
	team_member: string
	/**	Member Name : Data	*/
	member_name?: string
	/**	Is Supervisor : Check	*/
	is_supervisor?: 0 | 1
	/**	Supervisor : Link - Operation Team Member	*/
	parent_member?: string
	/**	Company : Link - Company	*/
	company: string
	/**	Image : Attach Image	*/
	image?: string
	/**	Left : Int	*/
	lft?: number
	/**	Old Parent : Link - Operation Team Member	*/
	old_parent?: string
	/**	Right : Int	*/
	rgt?: number
}