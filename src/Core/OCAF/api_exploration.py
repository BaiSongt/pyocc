# -*- coding: utf-8 -*-

"""
API Exploration Script for OCAF TFunction classes
This script explores the available methods and attributes of TFunction classes
to understand the correct API usage patterns.
"""

from OCC.Core.TFunction import TFunction_Driver, TFunction_Function, TFunction_Logbook
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Real
from OCC.Core.TDF import TDF_Label

def explore_tfunction_api():
    """Explore the TFunction API to understand correct usage patterns."""

    print("=== TFunction API Exploration ===\n")

    # 1. Explore TFunction_Logbook
    print("1. TFunction_Logbook methods:")
    logbook_methods = [method for method in dir(TFunction_Logbook) if not method.startswith('_')]
    for method in sorted(logbook_methods):
        print(f"   - {method}")
    print()

    # 2. Explore TFunction_Driver
    print("2. TFunction_Driver methods:")
    driver_methods = [method for method in dir(TFunction_Driver) if not method.startswith('_')]
    for method in sorted(driver_methods):
        print(f"   - {method}")
    print()

    # 3. Explore TFunction_Function
    print("3. TFunction_Function methods:")
    function_methods = [method for method in dir(TFunction_Function) if not method.startswith('_')]
    for method in sorted(function_methods):
        print(f"   - {method}")
    print()

    # 4. Try to create instances and see what works
    print("4. Testing instance creation:")

    try:
        # Try creating a logbook instance
        logbook = TFunction_Logbook()
        print("   ✓ TFunction_Logbook() constructor works")
        print(f"   Available logbook methods: {[m for m in dir(logbook) if not m.startswith('_') and 'Get' in m or 'Set' in m]}")
    except Exception as e:
        print(f"   ✗ TFunction_Logbook() constructor failed: {e}")

    try:
        # Try creating a driver instance
        driver = TFunction_Driver()
        print("   ✓ TFunction_Driver() constructor works")
    except Exception as e:
        print(f"   ✗ TFunction_Driver() constructor failed: {e}")

    # 4.1 Try to understand TFunction_Driver better
    print("\n4.1. TFunction_Driver class analysis:")
    print(f"   TFunction_Driver.__doc__: {TFunction_Driver.__doc__}")
    print(f"   TFunction_Driver.__bases__: {TFunction_Driver.__bases__}")

    # 4.2 Look for alternative ways to work with functions
    print("\n4.2. Looking for alternative approaches:")
    from OCC.Core.TFunction import TFunction_DriverTable
    print("   TFunction_DriverTable methods:")
    driver_table_methods = [method for method in dir(TFunction_DriverTable) if not method.startswith('_')]
    for method in sorted(driver_table_methods):
        print(f"     - {method}")

    # 5. Test with a document context
    print("\n5. Testing with document context:")

    try:
        doc = TDocStd_Document("test-doc")
        function_label = doc.Main().FindChild(1, True)

        # Try TFunction_Function.Set
        function_attr = TFunction_Function.Set(function_label)
        print("   ✓ TFunction_Function.Set() works")

        # Try to get the function
        function_attr_retrieved = TFunction_Function()
        if function_label.FindAttribute(TFunction_Function.GetID(), function_attr_retrieved):
            print("   ✓ TFunction_Function retrieval works")
        else:
            print("   ✗ TFunction_Function retrieval failed")

    except Exception as e:
        print(f"   ✗ Document context test failed: {e}")

def explore_tdatastd_api():
    """Explore TDataStd_Real API to understand correct usage."""
    print("\n=== TDataStd_Real API Exploration ===\n")

    from OCC.Core.TDataStd import TDataStd_Real

    print("TDataStd_Real methods:")
    real_methods = [method for method in dir(TDataStd_Real) if not method.startswith('_')]
    for method in sorted(real_methods):
        print(f"   - {method}")
    print()

    # Test with document context
    from OCC.Core.TDocStd import TDocStd_Document
    doc = TDocStd_Document("test")
    label = doc.Main().FindChild(1, True)

    # Set a real value
    TDataStd_Real.Set(label, 42.0)
    print("✓ TDataStd_Real.Set() works")

    # Try different ways to retrieve
    try:
        # Method 1: Try Find (static method)
        result = TDataStd_Real.Find(label)
        print(f"✓ TDataStd_Real.Find() works: {result}")
    except Exception as e:
        print(f"✗ TDataStd_Real.Find() failed: {e}")

    try:
        # Method 2: Try using FindAttribute with GetID
        attr = TDataStd_Real()
        found = label.FindAttribute(TDataStd_Real.GetID(), attr)
        if found:
            value = attr.Get()
            print(f"✓ FindAttribute method works: {value}")
        else:
            print("✗ FindAttribute method failed")
    except Exception as e:
        print(f"✗ FindAttribute method failed: {e}")

    # Method 3: Try to get the attribute directly from the label
    try:
        # Check if there's a more direct way
        attrs = []
        for i in range(1, 10):  # Check first few attribute IDs
            attr = TDataStd_Real()
            if label.FindAttribute(TDataStd_Real.GetID(), attr):
                attrs.append(attr.Get())
        print(f"Direct attribute values: {attrs}")
    except Exception as e:
        print(f"Direct method failed: {e}")

    # Method 4: Try to understand the issue with the value
    try:
        # Create a fresh label and test
        fresh_label = doc.Main().FindChild(2, True)
        TDataStd_Real.Set(fresh_label, 123.456)

        fresh_attr = TDataStd_Real()
        if fresh_label.FindAttribute(TDataStd_Real.GetID(), fresh_attr):
            fresh_value = fresh_attr.Get()
            print(f"Fresh attribute test: {fresh_value}")
    except Exception as e:
        print(f"Fresh attribute test failed: {e}")

if __name__ == "__main__":
    explore_tfunction_api()
    explore_tdatastd_api()
