
export interface DeliveryNoteItem{
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
	/**	Barcode : Data	*/
	barcode?: string
	/**	Has Item Scanned : Check	*/
	has_item_scanned?: 0 | 1
	/**	Item Code : Link - Item	*/
	item_code: string
	/**	Item Name : Data	*/
	item_name: string
	/**	Customer's Item Code : Data	*/
	customer_item_code?: string
	/**	Description : Text Editor	*/
	description?: string
	/**	Brand Name : Link - Brand	*/
	brand?: string
	/**	Item Group : Link - Item Group	*/
	item_group?: string
	/**	Image : Attach	*/
	image?: string
	/**	Image View : Image	*/
	image_view?: string
	/**	Quantity : Float	*/
	qty: number
	/**	Stock UOM : Link - UOM	*/
	stock_uom: string
	/**	UOM : Link - UOM	*/
	uom: string
	/**	UOM Conversion Factor : Float	*/
	conversion_factor: number
	/**	Qty in Stock UOM : Float	*/
	stock_qty?: number
	/**	Returned Qty in Stock UOM : Float	*/
	returned_qty?: number
	/**	Price List Rate : Currency	*/
	price_list_rate?: number
	/**	Price List Rate (Company Currency) : Currency	*/
	base_price_list_rate?: number
	/**	Margin Type : Select	*/
	margin_type?: "" | "Percentage" | "Amount"
	/**	Margin Rate or Amount : Float	*/
	margin_rate_or_amount?: number
	/**	Rate With Margin : Currency	*/
	rate_with_margin?: number
	/**	Discount (%) on Price List Rate with Margin : Float	*/
	discount_percentage?: number
	/**	Discount Amount : Currency	*/
	discount_amount?: number
	/**	Distributed Discount Amount : Currency	*/
	distributed_discount_amount?: number
	/**	Rate With Margin (Company Currency) : Currency	*/
	base_rate_with_margin?: number
	/**	Rate : Currency	*/
	rate?: number
	/**	Amount : Currency	*/
	amount?: number
	/**	Rate (Company Currency) : Currency	*/
	base_rate?: number
	/**	Amount (Company Currency) : Currency	*/
	base_amount?: number
	/**	Pricing Rules : Small Text	*/
	pricing_rules?: string
	/**	Rate of Stock UOM : Currency	*/
	stock_uom_rate?: number
	/**	Is Free Item : Check	*/
	is_free_item?: 0 | 1
	/**	Grant Commission : Check	*/
	grant_commission?: 0 | 1
	/**	Net Rate : Currency	*/
	net_rate?: number
	/**	Net Amount : Currency	*/
	net_amount?: number
	/**	Item Tax Template : Link - Item Tax Template	*/
	item_tax_template?: string
	/**	Net Rate (Company Currency) : Currency	*/
	base_net_rate?: number
	/**	Net Amount (Company Currency) : Currency	*/
	base_net_amount?: number
	/**	Billed Amt : Currency	*/
	billed_amt?: number
	/**	Incoming Rate : Currency	*/
	incoming_rate?: number
	/**	Weight Per Unit : Float	*/
	weight_per_unit?: number
	/**	Total Weight : Float	*/
	total_weight?: number
	/**	Weight UOM : Link - UOM	*/
	weight_uom?: string
	/**	Warehouse : Link - Warehouse	*/
	warehouse?: string
	/**	Target Warehouse : Link - Warehouse	*/
	target_warehouse?: string
	/**	Quality Inspection : Link - Quality Inspection	*/
	quality_inspection?: string
	/**	Allow Zero Valuation Rate : Check	*/
	allow_zero_valuation_rate?: 0 | 1
	/**	Against Sales Order : Link - Sales Order	*/
	against_sales_order?: string
	/**	Against Sales Order Item : Data	*/
	so_detail?: string
	/**	Against Sales Invoice : Link - Sales Invoice	*/
	against_sales_invoice?: string
	/**	Against Sales Invoice Item : Data	*/
	si_detail?: string
	/**	Against Delivery Note Item : Data	*/
	dn_detail?: string
	/**	Against Pick List : Link - Pick List	*/
	against_pick_list?: string
	/**	Pick List Item : Data	*/
	pick_list_item?: string
	/**	Serial and Batch Bundle : Link - Serial and Batch Bundle	*/
	serial_and_batch_bundle?: string
	/**	Use Serial No / Batch Fields : Check	*/
	use_serial_batch_fields?: 0 | 1
	/**	Serial No : Text	*/
	serial_no?: string
	/**	Batch No : Link - Batch	*/
	batch_no?: string
	/**	Qty (Warehouse) : Float	*/
	actual_qty?: number
	/**	Available Batch Qty at From Warehouse : Float	*/
	actual_batch_qty?: number
	/**	Qty (Company) : Float	*/
	company_total_stock?: number
	/**	Installed Qty : Float	*/
	installed_qty?: number
	/**	Packed Qty : Float	*/
	packed_qty?: number
	/**	Received Qty : Float	*/
	received_qty?: number
	/**	Expense Account : Link - Account	*/
	expense_account?: string
	/**	Item Tax Rate : Small Text	*/
	item_tax_rate?: string
	/**	Material Request : Link - Material Request	*/
	material_request?: string
	/**	Purchase Order : Link - Purchase Order	*/
	purchase_order?: string
	/**	Purchase Order Item : Data	*/
	purchase_order_item?: string
	/**	Material Request Item : Data	*/
	material_request_item?: string
	/**	Cost Center : Link - Cost Center	*/
	cost_center?: string
	/**	Project : Link - Project	*/
	project?: string
	/**	Page Break : Check	*/
	page_break?: 0 | 1
}