
export interface EmployeeEducation{
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
	/**	School/University : Small Text	*/
	school_univ?: string
	/**	Qualification : Data	*/
	qualification?: string
	/**	Level : Select	*/
	level?: "Graduate" | "Post Graduate" | "Under Graduate"
	/**	Year of Passing : Int	*/
	year_of_passing?: number
	/**	Class / Percentage : Data	*/
	class_per?: string
	/**	Major/Optional Subjects : Text	*/
	maj_opt_subj?: string
}