###############################################################################
#
# (C) Copyright 2020 Maikon Araujo
#
# This is an unpublished work containing confidential and proprietary
# information of Maikon Araujo. Disclosure, use, or reproduction
# without authorization of Maikon Araujo is prohibited.
#
###############################################################################

def instruments_to_csv(fname: str, ftype: str, dest_file: str): ...
def prices_to_csv(fname: str, ftype: str, dest_file: str): ...
def prices_to_mssql(
    fname: str, user: str, pwd: str, host: str, port: int, table: str, database: str
): ...
