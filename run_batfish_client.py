#!/usr/bin/env python


import json
import os
import pprint as pr

# Modules
from pybatfish.client.commands import bf_init_snapshot, bf_session
from pybatfish.question import bfq
from pybatfish.question.question import load_questions
from pybatfish.client.commands import *
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *
import pandas as pd

# Variables
bf_address = "127.0.0.1"

#reference_snapshot = "./snapshot"
reference_snapshot = "./snapshot_netdc_74"
output_dir = "./output/netdc_74"


# Body
def main():



    output_dir = "./output/netdc_74"

    # Create the directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)
    # Setting host to connect
    bf_session.host = bf_address

    # Loading confgs and questions
    bf_init_snapshot(reference_snapshot, overwrite=True)
    load_questions()

    # Running questions: below is node properties
    # ref: https://batfish.readthedocs.io/en/latest/notebooks/configProperties.html#Node-Properties
    r = bfq.nodeProperties().answer().frame()

    
    # Question I want overview route table
    folder_properties = "route_properties"

    folder_route_properties_out = prepare_output_dir(output_dir, folder_properties)
    routes_propertise = bfq.routes().answer().frame()
    routes_propertise.to_csv(f"{folder_route_properties_out}/routes.csv", index=False)
    # See column names
    routes_propertise_column = routes_propertise.columns
    routes_propertise_column.to_series().to_csv(
        f"{folder_route_properties_out}/routes_propereties_column.csv", index=False
    )

    
    #BGP Properties
    #ref: https://batfish.readthedocs.io/en/latest/notebooks/linked/introduction-to-bgp-analysis.html
    folder_properties = "bgp_properties"
    folder_bgp_properties_out = prepare_output_dir(output_dir, folder_properties)

    #bgp session  status
    bgpSessionStatus= bfq.bgpSessionStatus().answer().frame()
    bgpSessionStatus.to_csv(f"{folder_bgp_properties_out}/bgpSessionStatus.csv", index=False)
    bgpSessionCompatibility= bfq.bgpSessionCompatibility().answer().frame()
    bgpSessionCompatibility.to_csv(f"{folder_bgp_properties_out}/bgpSessionCompatibility.csv", index=False)

    # #Check bgp session compatibility with UNIQUE_MATCH physical ip fwsa0107-02_update.sxb1.gdg
    # bgpSessStat = bfq.bgpSessionStatus(nodes='fwsa0107-02_update.sxb1.gdg').answer().frame()
    # print(bgpSessStat)
    #  #Check bgp session compatibility with UNIQUE_MATCH physical ip fwsa0107-02_update.sxb1.gdg
    # bgpSessStat = bfq.bgpSessionStatus(nodes='fwsa0109-02_update.sxb1.gdg').answer().frame()
    # print(bgpSessStat)

    # ipOwn = bfq.ipOwners().answer().frame()
    # print(ipOwn[ipOwn['IP']=='10.242.65.222'])



    bgp_process = bfq.bgpProcessConfiguration().answer().frame()
    

    # see bgp rib
    bgp_rib = bfq.bgpRib().answer().frame()
    rib_filter = bgp_rib[(bgp_rib["Network"] == "10.253.4.71/32")]
    rib_filter.to_csv(
        f"{folder_bgp_properties_out}/bgp_rib_filter_network.csv", index=False
    )
    # print(bgp_rib)

    bgp_process_column = bgp_process.columns
    # print(bgp_process)



    bgp_rib.to_csv(f"{folder_bgp_properties_out}/bgp_rib.csv", index=False)

    bgp_peer = bfq.bgpPeerConfiguration().answer().frame()
    bgp_peer.to_csv(f"{folder_bgp_properties_out}/bgp_peer.csv", index=False)
    # Define the path to the CSV file
    csv_file = f"{folder_bgp_properties_out}/bgp_peer.csv"
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    # Filter the DataFrame
    filtered_df = df[df['Node'].isin(['lfgwsa0234-01', 'lfgwsa0338-01'])]
    # Output the filtered DataFrame to a new CSV file
    filtered_csv_file = f"{folder_bgp_properties_out}/filtered_bgp_peer.csv"
    filtered_df.to_csv(filtered_csv_file, index=False)
    # Further filter the DataFrame for Cluster_ID == True
    final_filtered_df = filtered_df[filtered_df['Cluster_ID'] == "True"]

    # Output the final filtered DataFrame to a new CSV file
    final_filtered_csv_file = f"{folder_bgp_properties_out}/final_filtered_bgp_peer.csv"
    final_filtered_df.to_csv(final_filtered_csv_file, index=False)
