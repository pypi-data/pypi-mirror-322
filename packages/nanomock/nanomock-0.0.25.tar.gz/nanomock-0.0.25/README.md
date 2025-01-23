# nanomock

A one click [nano-currency](https://nano.org) block-lattice environment on your local computer.
This project aims to easily spin up an integration environment with multiple nano nodes.
The local network is highly customizable.
All configuration is done inside the config file : `nanonet/nl_config.toml`

## prerequisites 

* python3.8+
* docker
* docker-compose 2

## Quickstart :

#### Install the library :

To install the library you can
- clone the respository and run `pip3 install .`
- or run `pip3 install nanomock`to download the latest version from PyPi

This gives you access to `nanomock {command}` command which will use `your_current_dir`as its entry point.

#### Spin up a network :

| Action            | Code                                              | Description  
| :----------       |:---------------------------------------------     | -----
| create            |`$ nanomock create`                                  | Create folders and node config 
| start             |`$ nanomock start`                                   | Start nodes (optional `--nodes`)
| init              |`$ nanomock init`                                    | Create Epochs Canary Burn and Vote weight distribution 
--------
#### Manage the network network :
| Action            | Code                                              | Description  
| :----------       |:---------------------------------------------     | -----
| status            |`$ nanomock status`                                  | Get status and block count for each node
| stop              |`$ nanomock stop`                                    | Stop nodes (optional `--nodes`)
| restart           |`$ nanomock restart`                                 | Restart all nodes  
| reset             |`$ nanomock reset`                                   | Delete data.ldb and wallets.ldb
| down              |`$ nanomock down`                                    | Remove all nodes
| destroy           |`$ nanomock destroy`                                 | Remove all nodes and data
| update            |`$ nanomock update `                                 | Pull and build latest containers

####  Query nodes :

Each node can be queried via RPC (see the [official documentation](https://docs.nano.org/commands/rpc-protocol/) )
| Action            | Code                                              | Description  
| :----------       |:---------------------------------------------     | -----
| rpc               |`$ nanomock rpc --payload '{"action" : "any_rpc"}'`  | Use nano_rpc commands (optional `--nodes`)


#### Configure the network :

`nl_config.toml` define all aspects of the network : genesis account, burn_amount, number of nodes, versions,...

