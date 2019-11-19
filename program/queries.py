import json, os
import relAlg

def select_supplier_name_s23_withBTree():
    table_name = relAlg.select("Suppliers", "sid", "=", "s23")
    relAlg.project(table_name,["sname"])
    return

def select_name_s23():
    table_name = relAlg.select("Suppliers", "sid", "=", "s23")
    relAlg.project("table_name",["sname"])
    return

def find_addresses_of_suppliers_who_supplied_p15():
    table_name = relAlg.join("Supply", "sid", "Suppliers", "sid")
    table_name_1 = relAlg.select(table_name, "pid", "=", "p15")
    relAlg.project(table_name_1, ["address"])
    return

def cost_of_p20_supplied_by_kiddie():
    table_name = relAlg.join("Supply", "sid", "Suppliers", "sid")
    table_name_1 = relAlg.select(table_name, "sname", "=", "Kiddie")
    relAlg.project(table_name_1, ["cost"])
    return

def fetch_sname_product_cost_for_cost_gte_47():
    table_name = relAlg.join("Supply", "sid", "Suppliers", "sid")
    table_name_1 = relAlg.join(table_name, "pid", "Products", "pid")
    table_name_2 = relAlg.select(table_name_1, "cost", ">=", "47")
    relAlg.project(table_name_2, ["sname", "pname", "cost"])
    return

# select_supplier_name_s23_withBTree()
# cost_of_p20_supplied_by_kiddie()
# find_addresses_of_suppliers_who_supplied_p15()
# fetch_sname_product_cost_for_cost_gte_47()