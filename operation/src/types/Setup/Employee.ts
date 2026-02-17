import { EmployeeEducation } from './EmployeeEducation'
import { EmployeeExternalWorkHistory } from './EmployeeExternalWorkHistory'
import { EmployeeInternalWorkHistory } from './EmployeeInternalWorkHistory'

export interface Employee{
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
	/**	Employee : Data	*/
	employee?: string
	/**	Series : Select	*/
	naming_series?: "HR-EMP-"
	/**	First Name : Data	*/
	first_name: string
	/**	Middle Name : Data	*/
	middle_name?: string
	/**	Last Name : Data	*/
	last_name?: string
	/**	Full Name : Data	*/
	employee_name?: string
	/**	Gender : Link - Gender	*/
	gender: string
	/**	Date of Birth : Date	*/
	date_of_birth: string
	/**	Salutation : Link - Salutation	*/
	salutation?: string
	/**	Date of Joining : Date	*/
	date_of_joining: string
	/**	Image : Attach Image	*/
	image?: string
	/**	Status : Select	*/
	status: "Active" | "Inactive" | "Suspended" | "Left"
	/**	User ID : Link - User - System User (login) ID. If set, it will become default for all HR forms.	*/
	user_id?: string
	/**	Create User Permission : Check - This will restrict user access to other employee records	*/
	create_user_permission?: 0 | 1
	/**	Company : Link - Company	*/
	company: string
	/**	Department : Link - Department	*/
	department?: string
	/**	Employee Number : Data	*/
	employee_number?: string
	/**	Designation : Link - Designation	*/
	designation?: string
	/**	Reports to : Link - Employee	*/
	reports_to?: string
	/**	Branch : Link - Branch	*/
	branch?: string
	/**	Offer Date : Date	*/
	scheduled_confirmation_date?: string
	/**	Confirmation Date : Date	*/
	final_confirmation_date?: string
	/**	Contract End Date : Date	*/
	contract_end_date?: string
	/**	Notice (days) : Int	*/
	notice_number_of_days?: number
	/**	Date Of Retirement : Date	*/
	date_of_retirement?: string
	/**	Mobile : Data	*/
	cell_number?: string
	/**	Personal Email : Data	*/
	personal_email?: string
	/**	Company Email : Data - Provide Email Address registered in company	*/
	company_email?: string
	/**	Prefered Contact Email : Select	*/
	prefered_contact_email?: "" | "Company Email" | "Personal Email" | "User ID"
	/**	Prefered Email : Data	*/
	prefered_email?: string
	/**	Unsubscribed : Check	*/
	unsubscribed?: 0 | 1
	/**	Current Address : Small Text	*/
	current_address?: string
	/**	Current Address Is : Select	*/
	current_accommodation_type?: "" | "Rented" | "Owned"
	/**	Permanent Address : Small Text	*/
	permanent_address?: string
	/**	Permanent Address Is : Select	*/
	permanent_accommodation_type?: "" | "Rented" | "Owned"
	/**	Emergency Contact Name : Data	*/
	person_to_be_contacted?: string
	/**	Emergency Phone : Data	*/
	emergency_phone_number?: string
	/**	Relation : Data	*/
	relation?: string
	/**	Attendance Device ID (Biometric/RF tag ID) : Data	*/
	attendance_device_id?: string
	/**	Holiday List : Link - Holiday List - Applicable Holiday List	*/
	holiday_list?: string
	/**	Cost to Company (CTC) : Currency	*/
	ctc?: number
	/**	Salary Currency : Link - Currency	*/
	salary_currency?: string
	/**	Salary Mode : Select	*/
	salary_mode?: "" | "Bank" | "Cash" | "Cheque"
	/**	Bank Name : Data	*/
	bank_name?: string
	/**	Bank A/C No. : Data	*/
	bank_ac_no?: string
	/**	IBAN : Data	*/
	iban?: string
	/**	Marital Status : Select	*/
	marital_status?: "" | "Single" | "Married" | "Divorced" | "Widowed"
	/**	Family Background : Small Text - Here you can maintain family details like name and occupation of parent, spouse and children	*/
	family_background?: string
	/**	Blood Group : Select	*/
	blood_group?: "" | "A+" | "A-" | "B+" | "B-" | "AB+" | "AB-" | "O+" | "O-"
	/**	Health Details : Small Text - Here you can maintain height, weight, allergies, medical concerns etc	*/
	health_details?: string
	/**	Passport Number : Data	*/
	passport_number?: string
	/**	Valid Upto : Date	*/
	valid_upto?: string
	/**	Date of Issue : Date	*/
	date_of_issue?: string
	/**	Place of Issue : Data	*/
	place_of_issue?: string
	/**	Bio / Cover Letter : Text Editor - Short biography for website and other publications.	*/
	bio?: string
	/**	Education : Table - Employee Education	*/
	education?: EmployeeEducation[]
	/**	External Work History : Table - Employee External Work History	*/
	external_work_history?: EmployeeExternalWorkHistory[]
	/**	Internal Work History : Table - Employee Internal Work History	*/
	internal_work_history?: EmployeeInternalWorkHistory[]
	/**	Resignation Letter Date : Date	*/
	resignation_letter_date?: string
	/**	Relieving Date : Date	*/
	relieving_date?: string
	/**	Exit Interview Held On : Date	*/
	held_on?: string
	/**	New Workplace : Data	*/
	new_workplace?: string
	/**	Leave Encashed? : Select	*/
	leave_encashed?: "" | "Yes" | "No"
	/**	Encashment Date : Date	*/
	encashment_date?: string
	/**	Reason for Leaving : Small Text	*/
	reason_for_leaving?: string
	/**	Feedback : Small Text	*/
	feedback?: string
	/**	lft : Int	*/
	lft?: number
	/**	rgt : Int	*/
	rgt?: number
	/**	Old Parent : Data	*/
	old_parent?: string
}