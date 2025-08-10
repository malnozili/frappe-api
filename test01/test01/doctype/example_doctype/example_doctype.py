import frappe
from frappe.model.document import Document


class ExampleDocType(Document):
    """Example DocType for API testing"""
    
    def validate(self):
        """Validate the document before saving"""
        if not self.title:
            frappe.throw("Title is required")
    
    def before_insert(self):
        """Set default values before inserting"""
        if not self.status:
            self.status = "Active"
    
    def after_insert(self):
        """Actions after document is inserted"""
        frappe.msgprint(f"Example record '{self.title}' created successfully")
    
    def before_save(self):
        """Actions before saving the document"""
        pass
    
    def after_save(self):
        """Actions after saving the document"""
        pass
    
    def before_delete(self):
        """Actions before deleting the document"""
        pass
    
    def after_delete(self):
        """Actions after deleting the document"""
        frappe.msgprint(f"Example record '{self.title}' deleted successfully")
