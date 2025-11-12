#!/usr/bin/env python3
"""
Test script for CRM - Supermercado El Sabanero Minimarket
Runs basic tests to verify functionality
"""

import os
import sys
from database import CRMDatabase

def test_database():
    """Test database operations"""
    print("Testing CRM Database...")
    print("-" * 60)
    
    # Use a test database
    test_db = "test_crm.db"
    
    # Remove test database if it exists
    if os.path.exists(test_db):
        os.remove(test_db)
    
    db = CRMDatabase(test_db)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Add customer
    print("\n1. Testing customer registration...")
    customer_id = db.add_customer("12345678", "Juan", "Test", "555-0001", "test@test.com", "Test St")
    if customer_id:
        print("   ✓ Customer added successfully (ID: {})".format(customer_id))
        tests_passed += 1
    else:
        print("   ✗ Failed to add customer")
        tests_failed += 1
    
    # Test 2: Get customer
    print("\n2. Testing customer retrieval...")
    customer = db.get_customer_by_cedula("12345678")
    if customer and customer['nombre'] == "Juan":
        print("   ✓ Customer retrieved successfully")
        tests_passed += 1
    else:
        print("   ✗ Failed to retrieve customer")
        tests_failed += 1
    
    # Test 3: Duplicate customer prevention
    print("\n3. Testing duplicate prevention...")
    duplicate_id = db.add_customer("12345678", "Juan", "Test", "555-0001", "test@test.com", "Test St")
    if duplicate_id is None:
        print("   ✓ Duplicate customer correctly prevented")
        tests_passed += 1
    else:
        print("   ✗ Duplicate customer was not prevented")
        tests_failed += 1
    
    # Test 4: Update customer
    print("\n4. Testing customer update...")
    updated = db.update_customer("12345678", telefono="555-9999")
    if updated:
        customer = db.get_customer_by_cedula("12345678")
        if customer['telefono'] == "555-9999":
            print("   ✓ Customer updated successfully")
            tests_passed += 1
        else:
            print("   ✗ Customer update failed")
            tests_failed += 1
    else:
        print("   ✗ Customer update failed")
        tests_failed += 1
    
    # Test 5: Add purchase
    print("\n5. Testing purchase registration...")
    compra_id = db.add_purchase(customer_id, 10000, "Efectivo")
    if compra_id:
        print("   ✓ Purchase added successfully (ID: {})".format(compra_id))
        tests_passed += 1
    else:
        print("   ✗ Failed to add purchase")
        tests_failed += 1
    
    # Test 6: Add purchase item
    print("\n6. Testing purchase item addition...")
    item_added = db.add_purchase_item(compra_id, "Test Product", 2, 5000)
    if item_added:
        print("   ✓ Purchase item added successfully")
        tests_passed += 1
    else:
        print("   ✗ Failed to add purchase item")
        tests_failed += 1
    
    # Test 7: Check loyalty points
    print("\n7. Testing loyalty points calculation...")
    customer = db.get_customer_by_cedula("12345678")
    expected_points = 10  # 10000 / 1000
    if customer['puntos_lealtad'] == expected_points:
        print("   ✓ Loyalty points calculated correctly ({} points)".format(expected_points))
        tests_passed += 1
    else:
        print("   ✗ Loyalty points incorrect (got {}, expected {})".format(
            customer['puntos_lealtad'], expected_points))
        tests_failed += 1
    
    # Test 8: Redeem points
    print("\n8. Testing points redemption...")
    redeemed = db.redeem_points(customer_id, 5, "Test redemption")
    if redeemed:
        customer = db.get_customer_by_cedula("12345678")
        if customer['puntos_lealtad'] == 5:  # 10 - 5
            print("   ✓ Points redeemed successfully")
            tests_passed += 1
        else:
            print("   ✗ Points balance incorrect after redemption")
            tests_failed += 1
    else:
        print("   ✗ Failed to redeem points")
        tests_failed += 1
    
    # Test 9: Prevent over-redemption
    print("\n9. Testing over-redemption prevention...")
    over_redeemed = db.redeem_points(customer_id, 1000, "Test over-redemption")
    if not over_redeemed:
        print("   ✓ Over-redemption correctly prevented")
        tests_passed += 1
    else:
        print("   ✗ Over-redemption was not prevented")
        tests_failed += 1
    
    # Test 10: Get purchase history
    print("\n10. Testing purchase history...")
    purchases = db.get_customer_purchases(customer_id)
    if len(purchases) == 1 and purchases[0]['total'] == 10000:
        print("   ✓ Purchase history retrieved correctly")
        tests_passed += 1
    else:
        print("   ✗ Purchase history incorrect")
        tests_failed += 1
    
    # Test 11: List customers
    print("\n11. Testing customer listing...")
    customers = db.list_all_customers()
    if len(customers) == 1:
        print("   ✓ Customer list retrieved correctly")
        tests_passed += 1
    else:
        print("   ✗ Customer list incorrect")
        tests_failed += 1
    
    # Test 12: Top customers
    print("\n12. Testing top customers report...")
    top_customers = db.get_top_customers(5)
    if len(top_customers) > 0:
        print("   ✓ Top customers report generated")
        tests_passed += 1
    else:
        print("   ✗ Top customers report failed")
        tests_failed += 1
    
    # Test 13: Sales summary
    print("\n13. Testing sales summary...")
    summary = db.get_sales_summary(30)
    if summary['total_compras'] == 1 and summary['total_ventas'] == 10000:
        print("   ✓ Sales summary calculated correctly")
        tests_passed += 1
    else:
        print("   ✗ Sales summary incorrect")
        tests_failed += 1
    
    # Clean up
    db.close()
    if os.path.exists(test_db):
        os.remove(test_db)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("Tests Passed: {}".format(tests_passed))
    print("Tests Failed: {}".format(tests_failed))
    print("Total Tests:  {}".format(tests_passed + tests_failed))
    print("Success Rate: {:.1f}%".format(100 * tests_passed / (tests_passed + tests_failed)))
    
    if tests_failed == 0:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(test_database())
