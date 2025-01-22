import logging
import sys

from ucampostgresvro import VERSION, utils
from ucampostgresvro.DBA import DB
from ucampostgresvro.exceptions import DbException
from ucampostgresvro.secrets import password


def setloggerdetail():
    LOG = logging.getLogger(__name__)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[stdout_handler],
    )
    return LOG


def main():
    LOG = setloggerdetail()
    LOG.info(f"VERSION : {VERSION}")
    db_params = {
        "dbname": "vrapricing",
        "user": "postgres",
        "password": password,
        "host": "infra-db.srv.uis.cam.ac.uk",  # or your database host
        "port": "5432",  # default PostgreSQL port
        "sslmode": "require",  # or 'verify-ca' or 'verify-full' based on your needs
        "sslrootcert": "./ca.crt",  # path to your client certificate
    }
    db = DB(db_params)

    if not utils.pre_setupconfig(db_params):
        raise DbException("ERROR: Tables are not created successfully")

    # db.insert_vrauser("ll220", "len")
    # print(db.get_vrauser("ll220"))
    # db.update_vrauser("ll220", "bda20", 'Ben Argyle')
    # print(db.get_vrauser())
    # db.remove_vrauser('bda20')
    # print(db.get_vrauser())

    # db.insert_deployment_id("1231ee112ad11212")
    # db.update_deployment_id("1231ee112ad11212", "1231a")
    # print(db.get_deployment_id("1231a"))
    # db.remove_deployment_id('1231a')
    # db.insert_deployment_id("123")
    # print(db.get_deployment_id())

    # print(db.get_project())
    # db.insert_project("0001",1,100.0)
    # db.insert_project("0101",2,100.0)
    # db.update_project("0001", "0002", 1, 200)
    # db.remove_project("0002")
    # db.insert_project("0001",1,100.0)
    # db.insert_project("0002",1,200.0)
    # print(db.get_project("0002",1,200))

    # print(db.get_grant())
    # db.insert_grant("0001",1,100.0)
    # db.update_grant("0001", "0002", 1, 200)
    # print(db.get_grant())
    # db.remove_grant("0002")
    # print(db.get_grant())
    # db.insert_grant("0001",1,100.0)
    # db.insert_grant("0002",1,200.0)
    # print(db.get_grant("0002",1,200))

    # print(db.get_costing())
    # db.insert_costing(1, "Initial Resource", project_id=2, grant_id=None)
    # db.insert_costing(1, "Initial Resource", project_id=None, grant_id=1)
    # db.update_costing(1, "Duration Expansion", old_grant_id=None,
    #                 old_project_id=2, grant_id=None, project_id=2)
    # print(db.get_costing())
    # print(db.get_costing())
    # db.remove_costing(1, "Duration Expansion", 4, None)
    # print(db.get_costing())

    db.closedb()


if __name__ == "__main__":
    main()
