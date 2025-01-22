import logging
from typing import Optional

import psycopg2

from ucampostgresvro.exceptions import DbException
from ucampostgresvro.tools import DEFAULT_TABLES

LOG = logging.getLogger(__name__)


class DB:
    def __init__(self, config: dict[str:str]) -> None:
        db_params = config
        self.connection = psycopg2.connect(**db_params)
        self.cursor = self.connection.cursor()

    def db_connection(self):
        """Provied the connection details of DB

        Returns:
            object: connection informtion of the DB
        """
        return self.connection

    def db_cursor(self):
        """Provied the cursor details of DB

        Returns:
            object: cursor informtion of the DB
        """
        return self.cursor

    def insert_vrauser(
        self, crsid: str, name: str, table_name: str = DEFAULT_TABLES.get("user")
    ) -> bool:
        """Insertion of the vrauser detail.

        Args:
            crsid (str): crsid of the user.
            name (str): name of the user.
            table_name (str): table name of the user.

        Raises:
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            if crsid and name:
                try:
                    self.cursor.execute(
                        f"INSERT INTO {table_name} (crsid, name) VALUES ('{crsid}', '{name}');"
                    )
                    LOG.info(
                        f"INFO: {table_name} insersion successful: CRSID {crsid} and Name {name}"
                    )
                    return True
                except Exception as e:
                    LOG.error(f"Error: {table_name} insertion : {e}")
                    return False
            else:
                LOG.error(
                    f"Error: Please provide both crid and name for {table_name} insertion"
                )
                raise DbException(f"Error: {table_name} insertion fail")

    def update_vrauser(
        self,
        old_crsid: str,
        new_crsid: str,
        name: str,
        table_name: str = DEFAULT_TABLES.get("user"),
    ) -> bool:
        """Updation of the vrauser.

        Args:
            old_crsid (str): CRSID which need to be updated.
            new_crsid (str): New CRSID which replaces the old CRSID.
            name (str): Name of the user
            table_name (str): table name of the user.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"UPDATE {table_name} SET crsid ='{new_crsid}' , name='{name}' WHERE crsid='{old_crsid}';"
                )
                LOG.info(f"INFO: {table_name} update successful for CRSID {old_crsid}")
                return True
            except Exception as e:
                LOG.error(f"Error: {table_name} Updating : {e}")
                return False

    def remove_vrauser(
        self, crsid: str, table_name: str = DEFAULT_TABLES.get("user")
    ) -> bool:
        """Removal of the vrauser.

        Args:
            crsid (str): CRSID need to be removed of the vrauser.
            table_name (str): table name of the user.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(f"DELETE from {table_name} WHERE crsid='{crsid}';")
                LOG.info(f"INFO: {table_name} removed CRSID {crsid} successfully.")
                return True
            except Exception as e:
                LOG.error(f"Error: {table_name} removing : {e}")
                return False

    def get_vrauser(
        self,
        crsid: Optional[str] = None,
        name: Optional[str] = None,
        table_name: str = DEFAULT_TABLES.get("user"),
    ) -> any:
        """Retreive the information from the vrauser table.

        Args:
            crsid (Optional[str], optional): CRSID need to be fetched. Defaults to None.
            name (Optional[str], optional): Name of the user to fetcb. Defaults to None.
            table_name (str): table name of the user.

        Returns:
            any: retreive the data from the vrauser database.
        """
        with self.connection:
            if crsid:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where crsid = '{crsid}';"
                )
            elif name:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where name = '{name}';"
                )
            elif crsid and name:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where crsid = '{crsid}' and name = '{name}';"
                )
            else:
                self.cursor.execute(f"SELECT * FROM {table_name};")
            LOG.info(f"INFO: {table_name} information is fetched successfully")
            return self.cursor.fetchall()

    def insert_deployment_id(
        self, deployment_id: str, table_name: str = DEFAULT_TABLES.get("deploymentid")
    ) -> bool:
        """Insertion of the deployment detail.

        Args:
            deployment_id (str): deployment ID information.
            table_name (str): table name of the deploymentid.

        Raises:
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            if deployment_id:
                try:
                    self.cursor.execute(
                        f"INSERT INTO {table_name} (deploymentID) VALUES ('{deployment_id}');"
                    )
                    LOG.info(
                        f"INFO: deployment ID {deployment_id} inserted successfully"
                    )
                    return True
                except Exception as e:
                    LOG.error(f"Error: deployment ID insertion in {table_name}: {e}")
                    return False
            else:
                LOG.error(
                    f"Error: Please provide deployment ID for {table_name} insertion"
                )
                raise DbException(
                    f"Error: Please provide deployment ID for {table_name} insertion"
                )

    def update_deployment_id(
        self,
        old_deployment_id: str,
        new_deployment_id: str,
        table_name: str = DEFAULT_TABLES.get("deploymentid"),
    ) -> bool:
        """Updation of the the deployment ID in deployment table.

        Args:
            old_deployment_id (str): Deployment ID which need to be updated.
            new_deployment_id (str): New Deployment ID which replaces the old Deployment ID.
            table_name (str): table name of the deploymentid.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"UPDATE {table_name} SET deploymentID ='{new_deployment_id}' \
                    WHERE deploymentID='{old_deployment_id}';"
                )
                LOG.info(
                    f"INFO: deployment ID of {old_deployment_id} updated successfully with \
                    {new_deployment_id} in table {table_name} ."
                )
                return True
            except Exception as e:
                LOG.error(f"Error: deployment ID update for table {table_name}: {e}")
                return False

    def remove_deployment_id(
        self, deployment_id: str, table_name: str = DEFAULT_TABLES.get("deploymentid")
    ) -> bool:
        """Removal of the deployment ID.

        Args:
            deployment_id (str): Deployment ID need to be removed from the Deployment table.
            table_name (str): table name of the deploymentid.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"DELETE from {table_name} WHERE deploymentID='{deployment_id}';"
                )
                LOG.info(
                    f"INFO: Removal of the deployment ID ' {deployment_id} ' has been performed successfully"
                )
                return True
            except Exception as e:
                LOG.error(
                    f"Error: deployment ID removing from table '{table_name}': {e}"
                )
                return False

    def get_deployment_id(
        self,
        deployment_id: Optional[str] = None,
        table_name: str = DEFAULT_TABLES.get("deploymentid"),
    ) -> any:
        """Retreive the information from the deployment table.

        Args:
            deployment_id (Optional[str], optional): Deployment ID need to be fetched. Defaults to None.
            table_name (str): table name of the deploymentid.

        Returns:
            any: Retreive the data from the Deployment ID database.
        """
        with self.connection:
            if deployment_id:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where deploymentID = '{deployment_id}';"
                )
            else:
                self.cursor.execute(f"SELECT * FROM {table_name};")
            LOG.info("INFO: deployment ID information is fetched successfully")
            return self.cursor.fetchall()

    def insert_project(
        self,
        project_number: str,
        paid_by: int,
        amount: float,
        table_name: str = DEFAULT_TABLES.get("proj"),
    ) -> bool:
        """Insertion of the project table.

        Args:
            project_number (str): payment order information.
            paid_by (int): primary key of the vrauser.
            amount (float): amount paid for the purchase.
            table_name (str): table name of the purchaseOrder.

        Raises:
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            if project_number:
                try:
                    self.cursor.execute(
                        f"INSERT INTO {table_name} (project_number, paid_by, amount) VALUES \
                            ('{project_number}', '{paid_by}', '{amount}');"
                    )
                    LOG.info(
                        f"INFO: Insertion of {project_number} and {amount} by {paid_by} is performed successfully"
                    )
                    return True
                except Exception as e:
                    LOG.error(
                        f"Error: project insertion in a table '{table_name}':\n {e}"
                    )
                    return False
            else:
                LOG.error(
                    "Error: Please provide project_number, paid_by, amount for Payment Oder"
                )
                raise DbException(
                    f"Error: project insertion fail in table {table_name}"
                )

    def update_project(
        self,
        old_project_number: str,
        new_project_number: str,
        new_paid_by: int,
        new_amount: float,
        table_name: str = DEFAULT_TABLES.get("proj"),
    ) -> bool:
        """Updation of the the project detail in project table

        Args:
            old_project_number (str): old payment order information.
            new_project_number (str): new payment order information to replace old payment order.
            new_paid_by (int): new primary key of the vrauser.
            new_amount (float): new amount paid for the purchase.
            table_name (str): table name of the purchaseOrder.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"UPDATE {table_name} SET \
                    project_number ='{new_project_number}', paid_by='{new_paid_by}', amount='{new_amount}' \
                    WHERE project_number='{old_project_number}';"
                )
                LOG.info(
                    f"INFO: Updation of the project {old_project_number} has been peformed successfully"
                )
                return True
            except Exception as e:
                LOG.error(f"Error: purchaseOrder Updating in table {table_name} : {e}")
                return False

    def remove_project(
        self, project_number: str, table_name: str = DEFAULT_TABLES.get("proj")
    ) -> bool:
        """Removal of the project.

        Args:
            project_number (str): project which need to be removed.
            table_name (str): table name of the purchaseOrder.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"DELETE from {table_name} WHERE project_number='{project_number}';"
                )
                LOG.info(
                    f"INFO: Removing of the project '{project_number}' has been performed successfully."
                )
                return True
            except Exception as e:
                LOG.error(
                    f"Error: purchaseOrder removing from table '{table_name}': {e}"
                )
                raise DbException(
                    f"Error: purchaseOrder removing from table '{table_name}': {e}"
                )

    def get_project(
        self,
        project_number: Optional[str] = None,
        table_name: str = DEFAULT_TABLES.get("proj"),
    ) -> any:
        """Retreive the information from the project table.

        Args:
            project_number (Optional[str], optional): project which need to be fetched. Defaults to None.
            table_name (str): table name of the purchaseOrder.

        Returns:
            any: Retreive the data from the project database.
        """
        with self.connection:
            if project_number:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where project_number = '{project_number}';"
                )
            else:
                self.cursor.execute(f"SELECT * FROM {table_name};")
            LOG.info("INFO: project information has been fetched successfully.")
            return self.cursor.fetchall()

    def insert_grant(
        self,
        grant_number: str,
        paid_by: int,
        amount: float,
        table_name: str = DEFAULT_TABLES.get("grant"),
    ) -> bool:
        """Insertion of the grant detail.

        Args:
            grant_number (str): grant information.
            paid_by (int):  primary key of the vrauser.
            amount (float): amount paid for the purchase.
            table_name (str): table name of the grant.


        Raises:
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            if grant_number:
                try:
                    self.cursor.execute(
                        f"INSERT INTO {table_name} (grant_number, paid_by, amount) \
                        VALUES ('{grant_number}', '{paid_by}', '{amount}');"
                    )
                    LOG.info(
                        f"INFO: Insertion of the grant {grant_number} and {amount} by \
                        {paid_by} has been performed successfully."
                    )
                    return True
                except Exception as e:
                    LOG.error(f"Error: grant Insert in table '{table_name}': {e}")
                    return False
            else:
                LOG.error(
                    "Error: Please provide grant_number, paid_by, amount for grants"
                )
                raise DbException(f"Error: grants insertion fail in table {table_name}")

    def update_grant(
        self,
        old_grant: str,
        new_grant: str,
        new_paid_by: int,
        new_amount: float,
        table_name: str = DEFAULT_TABLES.get("grant"),
    ) -> bool:
        """ "Updation of the the grant detail in grant table

        Args:
            old_grant (str): old grant information.
            new_grant (str): new grant information to replace old grant.
            new_paid_by (int): new primary key of the vrauser.
            new_amount (float): new amount paid for the purchase.
            table_name (str): table name of the grant.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"UPDATE {table_name} SET grant_number ='{new_grant}', paid_by='{new_paid_by}', \
                    amount='{new_amount}' WHERE grant_number='{old_grant}';"
                )
                LOG.info(
                    f"INFO: Updation of the grant {old_grant} has been performed successfully."
                )
                return True
            except Exception as e:
                LOG.error(
                    f"Error: grant Updating of '{old_grant}' in table '{table_name}': {e}"
                )
                return False

    def remove_grant(
        self, grant_number: str, table_name: str = DEFAULT_TABLES.get("grant")
    ) -> bool:
        """Removal of the grant.

        Args:
            grant_number (str): grant number which need to be replaced.
            table_name (str): table name of the grant.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            try:
                self.cursor.execute(
                    f"DELETE from {table_name} WHERE grant_number='{grant_number}';"
                )
                LOG.info(
                    f"INFO: Removal of the grant {grant_number} has been performed successfully."
                )
                return True
            except Exception as e:
                LOG.error(
                    f"Error: Removal of grant {grant_number} from table {table_name}: {e}"
                )
                raise DbException(
                    f"Error: Removal of grant {grant_number} from table {table_name}: {e}"
                )

    def get_grant(
        self,
        grant_number: str | None = None,
        table_name: str = DEFAULT_TABLES.get("grant"),
    ) -> any:
        """Retreive the information from the grant table.

        Args:
            grant_number (str | None, optional): grant which need to be fetched. Defaults to None.
            table_name (str): table name of the grant.

        Returns:
            any: Retreive the data from the grant database.
        """
        with self.connection:
            if grant_number:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where grant_number = '{grant_number}';"
                )
            else:
                self.cursor.execute(f"SELECT * FROM {table_name};")
            LOG.info("INFO: grant information has been fetched successfully.")
            return self.cursor.fetchall()

    def insert_costing(
        self,
        deployment_id: int,
        typee: str,
        project_id: Optional[int] = None,
        grant_id: Optional[int] = None,
        table_name: str = DEFAULT_TABLES.get("costing"),
    ) -> bool:
        """Insertion of the costing detail.

        Args:
            deployment_id (int): primary key of the deployment id.
            typee (str): type of the license.
            project_id (Optional[int], optional): primary key of the puchase order. Defaults to None.
            grant_id (Optional[int], optional): primary key of the grant. Defaults to None.
            table_name (str): table name of the costing.

        Raises:
            DbException: Exception for the provided inputs both PO and grant.
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            if project_id and grant_id:
                LOG.error(
                    "Error: Please do not provide both project_id &  grant_id for costing"
                )
                raise DbException(
                    "Error: Please do not provide both project_id &  grant_id for costing"
                )
            elif deployment_id and project_id and typee:
                try:
                    self.cursor.execute(
                        f"INSERT INTO {table_name} (deployment_id, type, project_id) VALUES \
                        ('{deployment_id}', '{typee}', '{project_id}');"
                    )
                    LOG.info("INFO: Costing insertion has been performed successfully")
                    return True
                except Exception as e:
                    LOG.error(
                        f"Error: cost removal failed in table '{table_name}': {e}"
                    )
                    return False
            elif deployment_id and grant_id and typee:
                try:
                    self.cursor.execute(
                        f"INSERT INTO {table_name} (deployment_id, type, grant_id) VALUES \
                        ('{deployment_id}', '{typee}',  '{grant_id}');"
                    )
                    LOG.info("INFO: Insertion of costing has been successfully")
                    return True
                except Exception as e:
                    LOG.error(
                        f"Error: cost removal failed in table '{table_name}': {e}"
                    )
                    return False
            else:
                LOG.error(
                    "Error: Please provide correct deployment_id, type, and, (project_id/grant_id) for costing"
                )
                raise DbException(
                    "Error: Please provide correct deployment_id, type, and, (project_id/grant_id) for costing"
                )

    def update_costing(
        self,
        deployment_id: int,
        typee: str,
        old_grant_id: Optional[int] = None,
        old_project_id: Optional[int] = None,
        grant_id: Optional[int] = None,
        project_id: Optional[int] = None,
        table_name: str = DEFAULT_TABLES.get("costing"),
    ) -> bool:
        """Updation of the costing database entry.

        Args:
            deployment_id (int): primary key of the deployment id.
            typee (str): type of the license.
            old_grant_id (Optional[int], optional): primary key of the old grant id. Defaults to None.
            old_project_id (Optional[int], optional): primary key of the old payment order. Defaults to None.
            grant_id (Optional[int], optional): primary key of the grant id. Defaults to None.
            project_id (Optional[int], optional): primary key of the grant id. Defaults to None.
            table_name (str): table name of the costing.

        Raises:
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        if old_project_id and old_grant_id:
            LOG.info(
                "Error: Please do not provide deployment_id. type, and, (project_id/ grant_id) for costing"
            )
            raise DbException(
                "Error: Please do not provide deployment_id. type, and, (project_id/ grant_id) for costing"
            )
        elif old_project_id:
            with self.connection:
                try:
                    grant_id = "NULL" if not grant_id else f"'{grant_id}'"
                    project_id = "NULL" if not project_id else f"'{project_id}'"
                    self.cursor.execute(
                        f"UPDATE {table_name} SET \
                        deployment_id ='{deployment_id}', type='{typee}', project_id={project_id}, \
                        grant_id={grant_id} WHERE project_id='{old_project_id}';"
                    )
                    LOG.info(
                        "INFO: updation of the costing has been performed successfully."
                    )
                    return True
                except Exception as e:
                    LOG.error(
                        f"Error: Updation of costing has failed in table '{table_name}': \n {e}"
                    )
                    return False
        elif old_grant_id:
            with self.connection:
                try:
                    grant_id = "NULL" if not grant_id else f"'{grant_id}'"
                    project_id = "NULL" if not project_id else f"'{project_id}'"
                    self.cursor.execute(
                        f"UPDATE {table_name} SET deployment_id ='{deployment_id}', type='{typee}', \
                        grant_id={grant_id}, project_id={project_id} WHERE grant_id='{old_grant_id}';"
                    )
                    LOG.info(
                        "INFO: updation of the costing has been performed successfully."
                    )
                    return True
                except Exception as e:
                    LOG.error(f"Error: Updation of costing has failed: \n {e}")
                    return False
        else:
            LOG.error("Error: updation of the costing has been failed")
            return False

    def remove_costing(
        self,
        deployment_id: int,
        typee: str,
        project_id: Optional[int] = None,
        grant_id: Optional[int] = None,
        table_name: str = DEFAULT_TABLES.get("costing"),
    ) -> bool:
        """Removal of the costing detail from costing database.

        Args:
            deployment_id (int): primary key of the deployment id.
            typee (str): type of the license.
            project_id (Optional[int], optional): primary key of the payment order. Defaults to None.
            grant_id (Optional[int], optional): primary key of the grant id. Defaults to None.
            table_name (str): table name of the costing.

        Raises:
            DbException: Exception for the provided inputs.

        Returns:
            bool: True for the success and False for the failure.
        """
        with self.connection:
            if grant_id and project_id:
                LOG.error(
                    "Error: Please do not provide both project_id and grant_id for costing"
                )
                raise DbException(
                    "Error: Please do not provide both project_id and grant_id for costing"
                )
            elif deployment_id and grant_id:
                try:
                    self.cursor.execute(
                        f"DELETE from {table_name} WHERE deployment_id = '{deployment_id}' and type = '{typee}' \
                        and grant_id = '{grant_id}';"
                    )
                    LOG.info(
                        "INFO: Removing of the costing has been performed successfully."
                    )
                    return True
                except Exception as e:
                    LOG.error(
                        f"Error: Removing of costing has failed in table {table_name}: \n {e}"
                    )
                    return False
            elif deployment_id and project_id:
                try:
                    self.cursor.execute(
                        f"DELETE from {table_name} WHERE deployment_id = '{deployment_id}' and type = '{typee}' \
                        and project_id = '{project_id}';"
                    )
                    LOG.info(
                        "INFO: Removing of the costing has been performed successfully."
                    )
                    return True
                except Exception as e:
                    LOG.error(
                        f"Error: Removing of costing has failed in table '{table_name}': \n {e}"
                    )
                    return False
            else:
                LOG.error(
                    "Error: Please provide correct deployment_id, type, and, (project_id/grant_id) for costing"
                )
                raise DbException(
                    "Error: Please provide correct deployment_id, type, and, (project_id/grant_id) for costing"
                )

    def get_costing(
        self,
        deployment_id: Optional[int] = None,
        typee: Optional[str] = None,
        project_id: Optional[int] = None,
        grant_id: Optional[int] = None,
        table_name: str = DEFAULT_TABLES.get("costing"),
    ) -> any:
        """Retreive the information from the costing table.

        Args:
            deployment_id (Optional[int], optional): primary key of the deployment id.. Defaults to None.
            typee (Optional[str], optional): type of the license.. Defaults to None.
            project_id (Optional[int], optional): primary key of the payment order. Defaults to None.
            grant_id (Optional[int], optional): primary key of the grant id. Defaults to None.
            table_name (str): table name of the costing.

        Returns:
            any: Retreive the data from the costing database.
        """
        with self.connection:
            if deployment_id and project_id and typee:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where deployment_id = '{deployment_id}' and type = '{typee}' \
                    and project_id = '{project_id}';"
                )
            elif deployment_id and grant_id and typee:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where deployment_id = '{deployment_id}' and type = '{typee}' \
                    and grant_id = '{grant_id}';"
                )
            elif deployment_id and not grant_id and not typee and not project_id:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where deployment_id = '{deployment_id}';"
                )
            elif not deployment_id and not grant_id and typee and not project_id:
                self.cursor.execute(
                    f"SELECT * FROM {table_name} where type = '{typee}';"
                )
            else:
                self.cursor.execute(f"SELECT * FROM {table_name};")
            LOG.info("INFO: costing information has been performed successfully")
            return self.cursor.fetchall()

    def closedb(self) -> None:
        """
        To close the databse connection.
        """
        self.connection.close()
