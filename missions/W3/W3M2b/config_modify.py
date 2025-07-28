import datetime
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import json

CONFIG_DIR = "config"
BACKUP_DIR = "config_backup"
MODIFICATIONS_FILE = os.path.join(CONFIG_DIR, "modifications.json")

def modify_config():
    with open(MODIFICATIONS_FILE, "r") as jf:
        MODIFICATIONS = json.load(jf)
        for fname, props in MODIFICATIONS.items():

            # backup config
            print(f"Backing up {backup_dir}...")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(BACKUP_DIR, ts)
            os.makedirs(backup_dir, exist_ok=True)
            src = os.path.join(CONFIG_DIR, fname)
            dst = os.path.join(backup_dir, fname)
            shutil.copy2(src, dst)

            #modify config
            print(f"Modifying up {backup_dir}...")
            path = os.path.join(CONFIG_DIR, fname)
            tree = ET.parse(path)
            root = tree.getroot()
            for prop in root.findall("property"):
                name = prop.findtext("name")
                if name in props:
                    old = prop.findtext("value")
                    new = props[name]
                    print(f"  - {name}: {old!r} → {new!r}")
                    prop.find("value").text = new

            tree.write(path, encoding="UTF-8", xml_declaration=True)

def verify_config():
    commands = [
        ['hdfs', 'getconf', '-confKey', 'fs.defaultFS'],
        ['hdfs', 'getconf', '-confKey', 'hadoop.tmp.dir'],
        ['hdfs', 'getconf', '-confKey', 'io.file.buffer.size'],
        ['hdfs', 'getconf', '-confKey', 'dfs.replication'],
        ['hdfs', 'getconf', '-confKey', 'dfs.blocksize'],
        ['hdfs', 'getconf', '-confKey', 'dfs.namenode.name.dir'],
        ['hadoop', 'getconf', '-confKey', 'mapreduce.framework.name'],
        ['hadoop', 'getconf', '-confKey', 'mapreduce.job.tracker'],
        ['hadoop', 'getconf', '-confKey', 'mapreduce.task.io.sort.mb'],
        ['yarn', 'getconf', '-confKey', 'yarn.resourcemanager.address'],
        ['yarn', 'getconf', '-confKey', 'yarn.nodemanager.resource.memory-mb'],
        ['yarn', 'getconf', '-confKey', 'yarn.scheduler.minimum-allocation-mb'],
    ]
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
            print(f"PASS: {' '.join(cmd)} -> {output}")
        except subprocess.CalledProcessError as e:
            print(f"FAIL: {' '.join(cmd)} -> {e}")
    # Replication factor check
    try:
        cmd = ["hdfs", "getconf", "-confKey", "dfs.replication"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        replication_value = result.stdout.strip()
        print(f"PASS: Replication factor is {replication_value}")
    except subprocess.CalledProcessError as e:
        print(f"FAIL: Replication factor check -> {e}")

def main():
    modify_config()

    print("Stopping Hadoop DFS...")
    subprocess.run(["docker", "compose", "restart"], check=True)
    print("Stopping YARN...")
    subprocess.run(["docker", "compose", "restart"], check=True)
    print("Starting Hadoop DFS...")
    subprocess.run(["docker", "compose", "restart"], check=True)
    print("Staring YARN")
    subprocess.run(["docker", "compose", "restart"], check=True)
    print("Configuration changes applied and services restarted.")

if __name__ == "__main__":
    main()