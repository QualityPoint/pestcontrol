import { DeliveryNoteItem } from './DeliveryNoteItem'
import { SalesTaxesandCharges } from '../Accounts/SalesTaxesandCharges'
import { PackedItem } from './PackedItem'
import { PricingRuleDetail } from '../Accounts/PricingRuleDetail'
import { SalesTeam } from '../Selling/SalesTeam'

export interface DeliveryNote{
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
	/**	Title : Data	*/
	title?: string
	/**	Series : Select	*/
	naming_series: "MAT-DN-.YYYY.-" | "MAT-DN-RET-.YYYY.-"
	/**	Customer : Link - Customer	*/
	customer: string
	/**	Tax Id : Data	*/
	tax_id?: string
	/**	Customer Name : Data	*/
	customer_name?: string
	/**	Date : Date	*/
	posting_date: string
	/**	Posting Time : Time	*/
	posting_time: string
	/**	Edit Posting Date and Time : Check	*/
	set_posting_time?: 0 | 1
	/**	Company : Link - Company	*/
	company: string
	/**	Amended From : Link - Delivery Note	*/
	amended_from?: string
	/**	Is Return : Check	*/
	is_return?: 0 | 1
	/**	Issue Credit Note : Check	*/
	issue_credit_note?: 0 | 1
	/**	Return Against Delivery Note : Link - Delivery Note	*/
	return_against?: string
	/**	Cost Center : Link - Cost Center	*/
	cost_center?: string
	/**	Project : Link - Project	*/
	project?: string
	/**	Currency : Link - Currency	*/
	currency: string
	/**	Exchange Rate : Float - Rate at which customer's currency is converted to company's base currency	*/
	conversion_rate: number
	/**	Price List : Link - Price List	*/
	selling_price_list: string
	/**	Price List Currency : Link - Currency	*/
	price_list_currency: string
	/**	Price List Exchange Rate : Float - Rate at which Price list currency is converted to company's base currency	*/
	plc_conversion_rate: number
	/**	Ignore Pricing Rule : Check	*/
	ignore_pricing_rule?: 0 | 1
	/**	Scan Barcode : Data	*/
	scan_barcode?: string
	/**	Last Scanned Warehouse : Data	*/
	last_scanned_warehouse?: string
	/**	Set Source Warehouse : Link - Warehouse	*/
	set_warehouse?: string
	/**	Set Target Warehouse : Link - Warehouse	*/
	set_target_warehouse?: string
	/**	Delivery Note Item : Table - Delivery Note Item	*/
	items: DeliveryNoteItem[]
	/**	Total Quantity : Float	*/
	total_qty?: number
	/**	Total Net Weight : Float	*/
	total_net_weight?: number
	/**	Total (Company Currency) : Currency	*/
	base_total?: number
	/**	Net Total (Company Currency) : Currency	*/
	base_net_total?: number
	/**	Total : Currency	*/
	total?: number
	/**	Net Total : Currency	*/
	net_total?: number
	/**	Tax Category : Link - Tax Category	*/
	tax_category?: string
	/**	Sales Taxes and Charges Template : Link - Sales Taxes and Charges Template	*/
	taxes_and_charges?: string
	/**	Shipping Rule : Link - Shipping Rule	*/
	shipping_rule?: string
	/**	Incoterm : Link - Incoterm	*/
	incoterm?: string
	/**	Named Place : Data	*/
	named_place?: string
	/**	Sales Taxes and Charges : Table - Sales Taxes and Charges	*/
	taxes?: SalesTaxesandCharges[]
	/**	Total Taxes and Charges (Company Currency) : Currency	*/
	base_total_taxes_and_charges?: number
	/**	Total Taxes and Charges : Currency	*/
	total_taxes_and_charges?: number
	/**	Grand Total (Company Currency) : Currency	*/
	base_grand_total?: number
	/**	Rounding Adjustment (Company Currency) : Currency	*/
	base_rounding_adjustment?: number
	/**	Rounded Total (Company Currency) : Currency	*/
	base_rounded_total?: number
	/**	In Words (Company Currency) : Data - In Words will be visible once you save the Delivery Note.	*/
	base_in_words?: string
	/**	Grand Total : Currency	*/
	grand_total?: number
	/**	Rounding Adjustment : Currency	*/
	rounding_adjustment?: number
	/**	Rounded Total : Currency	*/
	rounded_total?: number
	/**	In Words : Data - In Words (Export) will be visible once you save the Delivery Note.	*/
	in_words?: string
	/**	Disable Rounded Total : Check	*/
	disable_rounded_total?: 0 | 1
	/**	Apply Additional Discount On : Select	*/
	apply_discount_on?: "" | "Grand Total" | "Net Total"
	/**	Additional Discount Amount (Company Currency) : Currency	*/
	base_discount_amount?: number
	/**	Additional Discount Percentage : Float	*/
	additional_discount_percentage?: number
	/**	Additional Discount Amount : Currency	*/
	discount_amount?: number
	/**	Taxes and Charges Calculation : Text Editor	*/
	other_charges_calculation?: string
	/**	Packed Items : Table - Packed Item	*/
	packed_items?: PackedItem[]
	/**	Pricing Rule Detail : Table - Pricing Rule Detail	*/
	pricing_rules?: PricingRuleDetail[]
	/**	Billing Address Name : Link - Address	*/
	customer_address?: string
	/**	Billing Address : Small Text	*/
	address_display?: string
	/**	Contact Person : Link - Contact	*/
	contact_person?: string
	/**	Contact : Small Text	*/
	contact_display?: string
	/**	Mobile No : Small Text	*/
	contact_mobile?: string
	/**	Contact Email : Data	*/
	contact_email?: string
	/**	Shipping Address : Link - Address	*/
	shipping_address_name?: string
	/**	Shipping Address : Small Text	*/
	shipping_address?: string
	/**	Dispatch Address Name : Link - Address	*/
	dispatch_address_name?: string
	/**	Dispatch Address : Small Text	*/
	dispatch_address?: string
	/**	Company Address Name : Link - Address	*/
	company_address?: string
	/**	Company Address : Small Text	*/
	company_address_display?: string
	/**	Company Contact Person : Link - Contact	*/
	company_contact_person?: string
	/**	Terms : Link - Terms and Conditions	*/
	tc_name?: string
	/**	Terms and Conditions Details : Text Editor	*/
	terms?: string
	/**	% Amount Billed : Percent	*/
	per_billed?: number
	/**	Status : Select	*/
	status: "" | "Draft" | "To Bill" | "Partially Billed" | "Completed" | "Return" | "Return Issued" | "Cancelled" | "Closed"
	/**	% Installed : Percent	*/
	per_installed?: number
	/**	Installation Status : Select	*/
	installation_status?: string
	/**	% Returned : Percent	*/
	per_returned?: number
	/**	Transporter : Link - Supplier	*/
	transporter?: string
	/**	Driver : Link - Driver	*/
	driver?: string
	/**	Transport Receipt No : Data	*/
	lr_no?: string
	/**	Vehicle No : Data	*/
	vehicle_no?: string
	/**	Transporter Name : Data	*/
	transporter_name?: string
	/**	Driver Name : Data	*/
	driver_name?: string
	/**	Transport Receipt Date : Date	*/
	lr_date?: string
	/**	Customer's Purchase Order No : Small Text	*/
	po_no?: string
	/**	Customer's Purchase Order Date : Date	*/
	po_date?: string
	/**	Sales Partner : Link - Sales Partner	*/
	sales_partner?: string
	/**	Amount Eligible for Commission : Currency	*/
	amount_eligible_for_commission?: number
	/**	Commission Rate (%) : Float	*/
	commission_rate?: number
	/**	Total Commission : Currency	*/
	total_commission?: number
	/**	Sales Team : Table - Sales Team	*/
	sales_team?: SalesTeam[]
	/**	Auto Repeat : Link - Auto Repeat	*/
	auto_repeat?: string
	/**	Letter Head : Link - Letter Head	*/
	letter_head?: string
	/**	Print Without Amount : Check	*/
	print_without_amount?: 0 | 1
	/**	Group same items : Check	*/
	group_same_items?: 0 | 1
	/**	Print Heading : Link - Print Heading	*/
	select_print_heading?: string
	/**	Print Language : Data	*/
	language?: string
	/**	Is Internal Customer : Check	*/
	is_internal_customer?: 0 | 1
	/**	Represents Company : Link - Company - Company which internal customer represents.	*/
	represents_company?: string
	/**	Inter Company Reference : Link - Purchase Receipt	*/
	inter_company_reference?: string
	/**	Customer Group : Link - Customer Group	*/
	customer_group?: string
	/**	Territory : Link - Territory	*/
	territory?: string
	/**	Source : Link - Lead Source	*/
	source?: string
	/**	Campaign : Link - Campaign	*/
	campaign?: string
	/**	Excise Page Number : Data	*/
	excise_page?: string
	/**	Instructions : Text	*/
	instructions?: string
}