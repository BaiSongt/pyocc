# -*- coding: utf-8 -*-

"""
Simple test to understand TDataStd_Real usage
"""

from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TDataStd import TDataStd_Real
from OCC.Core.TDF import TDF_Attribute

def test_real_attribute():
    print("=== Testing TDataStd_Real ===")

    # Create document and label
    doc = TDocStd_Document("test")
    label = doc.Main().FindChild(1, True)

    # Set a value
    print("Setting value 42.5...")
    real_attr = TDataStd_Real.Set(label, 42.5)
    print(f"Set returned: {real_attr}")
    print(f"Set returned type: {type(real_attr)}")

    # Try to get the value directly from the returned attribute
    if real_attr:
        value = real_attr.Get()
        print(f"Direct value from Set(): {value}")

    # Try to retrieve the attribute later
    print("\nTrying to retrieve attribute later...")

    # Method 1: Try to get it again using Set (which should return existing)
    retrieved_attr = TDataStd_Real.Set(label, 0.0)  # This should return existing
    if retrieved_attr:
        value = retrieved_attr.Get()
        print(f"Retrieved via Set(): {value}")

    # Method 2: Try using a different label and see if we can cross-reference
    label2 = doc.Main().FindChild(2, True)
    attr2 = TDataStd_Real.Set(label2, 99.9)
    print(f"Second label value: {attr2.Get()}")

    # Method 3: Try to understand if we can store the attribute reference
    print("\nTesting attribute reference storage...")
    stored_attrs = {}
    stored_attrs['length'] = TDataStd_Real.Set(label, 100.0)
    stored_attrs['width'] = TDataStd_Real.Set(label2, 80.0)

    print(f"Stored length: {stored_attrs['length'].Get()}")
    print(f"Stored width: {stored_attrs['width'].Get()}")

    # Modify and check
    stored_attrs['length'].Set(150.0)
    print(f"Modified length: {stored_attrs['length'].Get()}")

    # Check if the modification persists when we get it again
    retrieved_again = TDataStd_Real.Set(label, 0.0)
    print(f"Retrieved after modification: {retrieved_again.Get()}")

if __name__ == "__main__":
    test_real_attribute()
