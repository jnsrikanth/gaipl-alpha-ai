import mysql.connector
from datetime import datetime, timedelta
import random
from typing import List, Dict

# Database configuration
db_config = {
    'host': 'db',
    'user': 'glpi',
    'password': 'glpi',
    'database': 'glpi',
    'auth_plugin': 'mysql_native_password'
}

# Define cloud components and their common issues
CLOUD_COMPONENTS = {
    'Azure': {
        'AKS': [
            'Node not ready',
            'Pod scheduling failed',
            'Service endpoint unreachable',
            'Container runtime errors',
            'Cluster autoscaling issues'
        ],
        'VM': [
            'High CPU utilization',
            'Disk space running low',
            'Network connectivity issues',
            'Memory leak detected',
            'Boot failure'
        ],
        'SQL MI': [
            'Performance degradation',
            'Backup failure',
            'High memory pressure',
            'Connectivity timeout',
            'Database corruption'
        ],
        'ASE': [
            'Web app not responding',
            'SSL certificate expired',
            'Worker process crashed',
            'Deployment failure',
            'Integration errors'
        ]
    },
    'GCP': {
        'GKE': [
            'Node pool autoscaling failed',
            'Load balancer misconfiguration',
            'Container image pull errors',
            'Network policy conflicts',
            'Control plane unresponsive'
        ],
        'Compute Engine': [
            'Instance terminated unexpectedly',
            'Network latency spike',
            'Disk I/O performance issues',
            'Resource quota exceeded',
            'Security group misconfiguration'
        ],
        'Cloud SQL': [
            'Replication lag',
            'Query performance degradation',
            'Storage capacity critical',
            'Backup validation failed',
            'Failover test failed'
        ]
    }
}

def generate_random_date(start_date: datetime, end_date: datetime) -> datetime:
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def generate_incidents(count: int) -> List[Dict]:
    incidents = []
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()

    for _ in range(count):
        cloud = random.choice(list(CLOUD_COMPONENTS.keys()))
        component = random.choice(list(CLOUD_COMPONENTS[cloud].keys()))
        issue = random.choice(CLOUD_COMPONENTS[cloud][component])

        created_date = generate_random_date(start_date, end_date)
        
        incident = {
            'name': f"{cloud} {component} - {issue}",
            'content': f"Alert: {issue} detected in {component}.\n\nDetailed Analysis:\n- Service affected: {cloud} {component}\n- Issue Description: {issue}\n- Potential root cause identified\n- Mitigation steps initiated",
            'priority': random.choice([1, 2, 3, 4, 5]),
            'urgency': random.choice([1, 2, 3, 4, 5]),
            'impact': random.choice([1, 2, 3, 4, 5]),
            'status': random.choice([1, 2, 3, 4, 5]),
            'date_creation': created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'date_mod': (created_date + timedelta(hours=random.randint(1, 48))).strftime('%Y-%m-%d %H:%M:%S'),
            'entities_id': 0,
            'type': 1,
            'itilcategories_id': 0
        }
        incidents.append(incident)
    
    return incidents

def insert_incidents(incidents: List[Dict]):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO glpi_tickets 
        (name, content, priority, urgency, impact, status, 
        date_creation, date_mod, entities_id, type, itilcategories_id) 
        VALUES 
        (%(name)s, %(content)s, %(priority)s, %(urgency)s, 
        %(impact)s, %(status)s, %(date_creation)s, %(date_mod)s, 
        %(entities_id)s, %(type)s, %(itilcategories_id)s)
        """

        for incident in incidents:
            cursor.execute(insert_query, incident)

        conn.commit()
        print(f"Successfully inserted {len(incidents)} incidents")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    incidents = generate_incidents(1000)
    insert_incidents(incidents)
