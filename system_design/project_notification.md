I'll explore the notification system to give you a comprehensive overview of how it works and what each file does.
Read file: chatbook-backend/notifications/models.py
Read file: chatbook-backend/notifications/outbox.py
Read file: chatbook-backend/notifications/signals.py
Read file: chatbook-backend/notifications/publisher.py

Read file: chatbook-backend/notifications/services.py
Read file: chatbook-backend/notifications/template_config.py
Read file: chatbook-backend/notifications/views.py
Read file: chatbook-backend/notifications/admin.py

Based on my exploration of the notifications directory, here's a comprehensive overview of the notification system architecture and how each file contributes to the overall functionality:

## 🔔 **Notification System Overview**

The chatbook-backend implements a **robust, event-driven notification system** using the **Outbox Pattern** for reliable message delivery. It supports both **email notifications** (via AWS SES) and **push notifications** (via AWS SNS → Lambda → APNs) with transactional consistency guarantees.

### 📋 **System Architecture**

```
Django App Event → Outbox Event → Publisher → AWS SNS → Lambda → Email/Push
                ↳ Signals      ↳ Retry Logic   ↳ Templates  ↳ Multi-channel
```

---

## 📁 **File-by-File Breakdown**

### **1. `models.py` (171 lines) - Data Layer**
**Purpose**: Defines the core data structures for the notification system

**Key Models**:
- **`OutboxEvent`**: Core model implementing the outbox pattern
  - UUID primary keys with sequence numbers for ordering
  - Status tracking (`pending` → `processing` → `published`/`failed`/`dead_letter`)
  - Retry logic with exponential backoff (max 5 minutes)
  - Event types: `appointment.booked`, `appointment.changed`, `appointment.cancelled`, etc.
  - JSON payload and metadata storage
- **`DeviceToken`**: Stores iOS device tokens for push notifications
  - User-linked with unique token constraint
  - Active/inactive status tracking

---

### **2. `outbox.py` (515 lines) - Outbox Pattern Implementation**
**Purpose**: Provides transactional consistency between domain operations and event publishing

**Key Features**:
- **`OutboxService`**: Main service class for creating events
- **Event Creation Methods**:
  - `create_event()`: Generic event creation
  - `create_appointment_event()`: Appointment-specific events with business context
  - `create_appointment_event_consolidated()`: Prevents duplicate events within 5-second window
- **Event Consolidation**: Uses Redis caching to merge rapid successive changes
- **Transactional Safety**: All event creation happens within database transactions

---

### **3. `signals.py` (371 lines) - Event Triggers**
**Purpose**: Django signal handlers that automatically create outbox events when domain events occur

**Key Signal Handlers**:
- **Appointment Events**:
  - `post_save` on `Appointment` → `appointment.booked` (new) or `appointment.changed` (updates)
  - `post_delete` on `Appointment` → `appointment.cancelled`
- **Service/AddOn Changes**: Tracks modifications to appointment services and add-ons
- **Waitlist Events**: `waitlist.entry_created` when users join waitlists
- **Change Tracking**: `AppointmentChangeTracker` class preserves old values for comparison
- **Consolidation Logic**: Prevents duplicate events during rapid successive changes

---

### **4. `publisher.py` (1074 lines) - Event Processing Engine**
**Purpose**: Polls outbox events and publishes them to AWS SNS with sophisticated retry logic

**Key Components**:
- **`OutboxPublisher`**: Main publisher class
- **Processing Pipeline**:
  1. Fetches pending events in batches (default: 50)
  2. Routes events by type (`appointment.*`, `waitlist.*`, `notification.*`)
  3. Builds multi-recipient notification messages
  4. Publishes to AWS SNS with structured JSON payloads
- **Multi-Recipient Support**: Single event can notify multiple users (business + customer)
- **Template Integration**: Selects appropriate email templates per user type
- **Error Handling**: Comprehensive retry logic with dead letter handling

---

### **5. `services.py` (281 lines) - AWS Integration Layer**
**Purpose**: Handles AWS SNS communication and push notification logic

**Key Features**:
- **`NotificationService`**: AWS SNS client wrapper
- **Multi-Environment Support**: Handles AWS profiles, regions, credentials
- **Push Notification Methods**:
  - `notify_user()`: Single user notifications
  - `notify_users()`: Batch user notifications
- **Device Token Management**: Validates and manages iOS device tokens
- **Error Handling**: Comprehensive AWS error handling with fallbacks
- **Configuration Detection**: Auto-detects SNS topic ARN from environment

---

### **6. `template_config.py` (163 lines) - Email Template Management**
**Purpose**: Defines email template mappings and recipient configurations

**Key Configurations**:
- **Template Directories**:
  - `business_templates/`: Templates for business users
  - `customer_templates/`: Templates for customers
- **Event-to-Template Mapping**: Maps each event type to appropriate templates
- **Recipient Rules**: Defines who receives notifications for each event type
  - `appointment.booked`: Both business and customer
  - `appointment.reminder`: Customer only
- **Template Resolution**: `get_email_template_key()` builds S3 template paths

---

### **7. `views.py` (170 lines) - API Endpoints**
**Purpose**: REST API endpoints for device registration and notification management

**API Endpoints**:
- **`POST /register_device`**: Register iOS device tokens for push notifications
  - Validates token format (10-200 characters)
  - Uses `update_or_create` to handle duplicates
  - Returns registration status
- **`POST /deactivate_device`**: Deactivate device tokens
  - Soft delete approach (sets `is_active=False`)
  - User-scoped token management
- **Error Handling**: Comprehensive validation and database error handling

---

### **8. `admin.py` (163 lines) - Django Admin Interface**
**Purpose**: Administrative interface for monitoring and managing notifications

**Admin Features**:
- **OutboxEvent Admin**:
  - List view with status, retry count, timestamps
  - Filtering by status, event type, date ranges
  - Search by ID, event type, error messages
  - Bulk actions: retry failed events, mark as dead letter
  - Formatted JSON payload display
- **DeviceToken Admin**:
  - User association tracking
  - Active/inactive status management
  - Token registration history

---

### **9. Supporting Files**

- **`apps.py`**: Django app configuration
- **`urls.py`**: URL routing for API endpoints
- **`tests.py`**: Comprehensive test suite for notification functionality
- **`__init__.py`**: Package initialization

---

## 🔄 **Event Flow Example**

1. **User books appointment** → Django saves `Appointment`
2. **Signal handler** → Creates `OutboxEvent` with `appointment.booked` type
3. **Publisher polls** → Finds pending event, marks as `processing`
4. **Template resolution** → Determines business/customer email templates
5. **SNS publishing** → Sends structured JSON to AWS SNS topic
6. **Lambda processing** → AWS Lambda receives message, sends emails/push notifications
7. **Status update** → Event marked as `published` with SNS MessageId

## 🛡️ **Reliability Features**

- **Transactional Consistency**: Outbox pattern ensures no lost events
- **Retry Logic**: Exponential backoff up to 5 minutes
- **Dead Letter Handling**: Failed events moved to dead letter status
- **Event Consolidation**: Prevents spam from rapid successive changes
- **Comprehensive Logging**: Full audit trail of all notification activities
- **Multi-Channel Support**: Email (SES) + Push (APNs) notifications

This notification system provides **enterprise-grade reliability** with **multi-tenant support**, making it suitable for a production SaaS application serving multiple beauty businesses.