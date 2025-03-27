#!/usr/bin/env python3
"""
Script to generate fake change data for GLPI that correlates with incidents.
Generates 6000 changes over the last 365 days with realistic changes reflecting
existing infrastructure like Azure VM, AKS, Azure SQL, GCP, GKE, etc.
"""

import MySQLdb
import random
import logging
import datetime
import gc
import os
from datetime import timedelta

# Configure logging - minimal output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Disable verbose logging from other modules
logging.getLogger("MySQLdb").setLevel(logging.WARNING)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'db'),
    'user': os.getenv('DB_USER', 'glpi'),
    'password': os.getenv('DB_PASSWORD', 'glpi'),
    'database': os.getenv('DB_NAME', 'glpi')
}

# Constants
TOTAL_CHANGES = 6000
BATCH_SIZE = 100

# GLPI status mappings
STATUS_MAPPING = {
    'new': 1,
    'planning': 2,
    'approval': 3,
    'approved': 4,
    'waiting': 5,
    'in_progress': 6,
    'applied': 7,
    'review': 8,
    'closed': 6,  # Matching closed status in GLPI
}

# GLPI priority, impact, urgency mappings
PRIORITY_MAPPING = {
    'very_low': 1,
    'low': 2,
    'medium': 3,
    'high': 4,
    'very_high': 5
}

# Global validation states
VALIDATION_MAPPING = {
    'none': 0,
    'pending': 1,
    'accepted': 2,
    'rejected': 3
}

# Cloud infrastructure change types
CHANGE_TYPES = [
    {
        "type": "Azure VM",
        "scenarios": [
            "OS upgrade",
            "Network configuration update",
            "Storage expansion",
            "Security hardening",
            "Instance type upgrade",
            "High availability configuration"
        ]
    },
    {
        "type": "Azure AKS",
        "scenarios": [
            "Kubernetes version upgrade",
            "Node pool expansion",
            "Security policy implementation",
            "Networking configuration update",
            "Autoscaling implementation",
            "Container registry integration"
        ]
    },
    {
        "type": "Azure SQL",
        "scenarios": [
            "Database performance tuning",
            "Storage allocation increase",
            "Backup policy update",
            "High availability configuration",
            "Security audit implementation",
            "Query optimization"
        ]
    },
    {
        "type": "Azure SQL MI",
        "scenarios": [
            "Instance sizing update",
            "Storage allocation increase",
            "Read replica deployment",
            "Geo-replication setup",
            "Backup retention policy update",
            "Performance tier upgrade"
        ]
    },
    {
        "type": "Azure ASE",
        "scenarios": [
            "App Service scaling",
            "Runtime version upgrade",
            "Network integration update",
            "SSL certificate rotation",
            "Custom domain configuration",
            "Autoscale settings modification"
        ]
    },
    {
        "type": "GCP VM",
        "scenarios": [
            "Instance resize",
            "OS patching",
            "Network interface update",
            "Startup script modification",
            "Managed instance group update"
        ]
    },
    {
        "type": "GCP GKE",
        "scenarios": [
            "Cluster upgrade",
            "Node auto-provisioning setup",
            "Pod security policy implementation",
            "Network policy update",
            "Workload identity configuration"
        ]
    },
    {
        "type": "GCP Cloud SQL",
        "scenarios": [
            "Instance scaling",
            "Maintenance window adjustment",
            "High availability configuration",
            "Backup retention policy update",
            "Read replica creation"
        ]
    }
]

def get_db_connection():
    """Establish a database connection"""
    try:
        connection = MySQLdb.connect(**db_config)
        return connection
    except MySQLdb.Error as e:
        logger.error("Error connecting to database: %s", e)
        raise

def get_random_date(days_back=365):
    """Generate a random date within the specified days back from today"""
    today = datetime.datetime.now()
    random_days = random.randint(1, days_back)
    random_date = today - datetime.timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def fetch_incidents(connection, limit=1000):
    """Fetch existing incidents from the database to correlate with changes"""
    cursor = connection.cursor()
    
    try:
        query = """
        SELECT id, name, content, date, entities_id, priority 
        FROM glpi_tickets 
        WHERE type = 1 
        ORDER BY RAND() 
        LIMIT %s
        """
        cursor.execute(query, (limit,))
        incidents = cursor.fetchall()
        logger.info("Fetched %d incidents for correlation", len(incidents))
        return incidents
    except MySQLdb.Error as e:
        logger.error("Error fetching incidents: %s", e)
        return []
    finally:
        cursor.close()

def generate_change_content(change_type, activity, related_incidents):
    """Generate detailed content for the change."""
    incident_references = []
    for inc in related_incidents:
        incident_references.append("- Related to Incident #{0}: {1}".format(inc[0], inc[1]))
    incident_text = "\n".join(incident_references)
    
    objectives = [
        "Implement {0} {1} to improve system stability".format(change_type, activity),
        "Resolve underlying issues identified in related incidents",
        "Enhance performance and reliability of the {0} infrastructure".format(change_type),
        "Apply industry best practices for {0} configuration".format(change_type)
    ]
    
    implementation_plan = [
        "1. Conduct pre-implementation testing in development environment",
        "2. Schedule maintenance window for {0} modifications".format(change_type),
        "3. Create system backup and verify recovery procedures",
        "4. Implement {0} according to documented procedures".format(activity),
        "5. Validate functionality and performance post-implementation",
        "6. Update documentation and knowledge base articles"
    ]
    
    impact_assessment = [
        "Affected Systems: {0} infrastructure and dependent services".format(change_type),
        "User Impact: Minimal to moderate during implementation window",
        "Service Interruption: 15-30 minutes expected during cutover phase",
        "Recovery Plan: Rollback to previous configuration if issues detected"
    ]
    
    content = """
## Change Summary
Implement {0} - {1}

## Related Incidents
{2}

## Objectives
{3}

## Implementation Plan
{4}

## Impact Assessment
{5}
""".format(
        change_type, 
        activity, 
        incident_text, 
        random.choice(objectives),
        random.choice(implementation_plan),
        random.choice(impact_assessment)
    )
    
    return content

def generate_change_data(incidents, index):
    """Generate a single change record with correlation to incidents"""
    if not incidents:
        logger.warning("No incidents available for correlation")
        return None
    
    # Get random incident to correlate with
    num_related_incidents = random.randint(1, min(3, len(incidents)))
    related_incidents = random.sample(incidents, num_related_incidents)
    primary_incident = related_incidents[0]
    incident_id, incident_name, incident_content, incident_date, entities_id, incident_priority = primary_incident
    
    # Select random change type and scenario
    change_type_data = random.choice(CHANGE_TYPES)
    change_type = change_type_data["type"]
    scenario = random.choice(change_type_data["scenarios"])
    
    # Generate dates
    creation_date = get_random_date()
    
    # Create change name and content
    name = "{0} - {1}".format(change_type, scenario)
    content = generate_change_content(change_type, scenario, related_incidents)
    
    # Select random status
    status_options = list(STATUS_MAPPING.keys())
    status_text = random.choice(status_options)
    status = STATUS_MAPPING.get(status_text, 1)  # Default to 'new' if not found
    
    # Select random priority, impact, urgency based on related incident
    priority_options = list(PRIORITY_MAPPING.keys())
    
    # Try to correlate priority with the incident priority
    adjusted_priority_index = min(max(0, incident_priority - 1), len(priority_options) - 1)
    priority_range_start = max(0, adjusted_priority_index - 1)
    priority_range_end = min(len(priority_options), adjusted_priority_index + 2)
    priority_text = random.choice(priority_options[priority_range_start:priority_range_end])
    priority = PRIORITY_MAPPING.get(priority_text, 3)  # Default to medium
    
    impact_text = random.choice(priority_options)
    impact = PRIORITY_MAPPING.get(impact_text, 3)
    
    urgency_text = random.choice(priority_options)
    urgency = PRIORITY_MAPPING.get(urgency_text, 3)
    
    # Global validation based on status
    if status_text in ['approved', 'in_progress', 'applied', 'review', 'closed']:
        validation = 'accepted'
    elif status_text == 'approval':
        validation = 'pending'
    else:
        validation = 'none'
    
    global_validation = VALIDATION_MAPPING.get(validation, 0)
    
    # Create the change dictionary
    change = {
        'name': name,
        'content': content,
        'entities_id': entities_id,
        'date': creation_date,
        'date_mod': creation_date,
        'status': status,
        'priority': priority,
        'urgency': urgency,
        'impact': impact,
        'global_validation': global_validation,
        'users_id_recipient': 2,  # Default admin user
        'users_id_lastupdater': 2,  # Default admin user
        'related_incident_ids': [inc[0] for inc in related_incidents]
    }
    
    return change

def insert_batch(connection, changes):
    """Insert a batch of changes into the database"""
    if not changes:
        return 0
    
    cursor = connection.cursor()
    successful_inserts = 0
    
    try:
        for change in changes:
            # Insert the change record
            insert_query = """
            INSERT INTO glpi_changes 
            (name, content, entities_id, date, date_mod, status, 
            priority, urgency, impact, global_validation, 
            users_id_recipient, users_id_lastupdater) 
            VALUES 
            (%(name)s, %(content)s, %(entities_id)s, %(date)s, %(date_mod)s, 
            %(status)s, %(priority)s, %(urgency)s, %(impact)s, %(global_validation)s, 
            %(users_id_recipient)s, %(users_id_lastupdater)s)
            """
            
            cursor.execute(insert_query, {
                'name': change['name'],
                'content': change['content'],
                'entities_id': change['entities_id'],
                'date': change['date'],
                'date_mod': change['date_mod'],
                'status': change['status'],
                'priority': change['priority'],
                'urgency': change['urgency'],
                'impact': change['impact'],
                'global_validation': change['global_validation'],
                'users_id_recipient': change['users_id_recipient'],
                'users_id_lastupdater': change['users_id_lastupdater']
            })
            
            change_id = cursor.lastrowid
            
            # Create relationship to incidents
            for incident_id in change['related_incident_ids']:
                relation_query = """
                INSERT INTO glpi_changes_tickets 
                (changes_id, tickets_id) 
                VALUES (%s, %s)
                """
                cursor.execute(relation_query, (change_id, incident_id))
            
            successful_inserts += 1
        
        connection.commit()
        return successful_inserts
    except MySQLdb.Error as e:
        connection.rollback()
        logger.error("Error inserting changes: %s", e)
        return successful_inserts
    finally:
        cursor.close()

def main():
    """Main function to generate and insert changes"""
    start_time = datetime.datetime.now()
    logger.info("Starting change generation process for %d changes", TOTAL_CHANGES)
    
    try:
        # Connect to the database
        connection = get_db_connection()
        
        # Fetch incidents to correlate with changes
        incidents = fetch_incidents(connection)
        if not incidents:
            logger.error("No incidents found to correlate with changes. Exiting.")
            return
        
        logger.info("Found %d incidents for correlation", len(incidents))
        
        # Generate and insert changes in batches
        total_inserted = 0
        
        for batch_start in range(0, TOTAL_CHANGES, BATCH_SIZE):
            batch_end = min(batch_start + BATCH_SIZE, TOTAL_CHANGES)
            current_batch_size = batch_end - batch_start
            
            # Only log at 10% intervals or first/last batch
            progress_pct = (batch_start / TOTAL_CHANGES) * 100
            if progress_pct % 10 == 0 or batch_start == 0 or batch_end == TOTAL_CHANGES:
                logger.info("Generating batch %d-%d of %d changes (%.1f%%)", 
                           batch_start + 1, batch_end, TOTAL_CHANGES, progress_pct)
            
            # Generate batch of changes
            changes_batch = []
            for i in range(current_batch_size):
                change = generate_change_data(incidents, batch_start + i)
                if change:
                    changes_batch.append(change)
            
            # Insert batch of changes
            successful_inserts = insert_batch(connection, changes_batch)
            total_inserted += successful_inserts
            
            # Only log at 10% intervals or first/last batch
            completion_percentage = (total_inserted / TOTAL_CHANGES) * 100
            if completion_percentage % 10 < (BATCH_SIZE / TOTAL_CHANGES) * 100 or batch_end == TOTAL_CHANGES:
                logger.info("Progress: %d/%d changes inserted (%.1f%%)", 
                           total_inserted, TOTAL_CHANGES, completion_percentage)
            
            # Clean up memory
            del changes_batch
            gc.collect()
        
        # Log final summary
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info("Change generation complete: %d/%d changes in %.2f seconds (%.2f changes/sec)", 
                   total_inserted, TOTAL_CHANGES, duration, total_inserted/duration if duration > 0 else 0)

    except Exception as e:
        logger.error("Error during change generation: %s", e)
    finally:
        if 'connection' in locals():
            connection.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    main()
