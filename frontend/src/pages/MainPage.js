import {useEffect, useState} from "react";
import {Box, Button, Modal, Tab, TextField, Typography} from "@mui/material";
import {Tabs} from "@mui/material"
import ListInventory from "../components/ListInventory";
import PaginationInventory from "../components/PaginationInventory";

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 600,
    height: 250,
    bgcolor: 'background.paper',
    boxShadow: 24,
    p: 4,
};

const MainPage = () => {
    const [tab, setTab] = useState(1);
    const [inventories, setInventories] = useState(null);
    const [paging, setPaging] = useState({
        items_per_page: 0,
        page: 0,
        total: 0
    });
    const [name, setName] = useState(null)
    const [inventoryName, setInventoryName] = useState("");
    const [inventoryAmount, setInventoryAmount] = useState(null);
    const [addModal, setAddModal] = useState(false);

    const inventoryURL = `${process.env.REACT_APP_API_DOMAIN}/inventory`;
    const delInventoryURL = `${process.env.REACT_APP_API_DOMAIN}/inventory/delete`;

    const changeTab = (event, newTab) => {
        setTab(newTab);
    }

    const fetchData = (url) => {
        fetch(url).then(response => {
            response.json().then(data => {
                if (data.status_code === 200) {
                    setInventories(data.data.inventory);
                    setPaging(data.data.paging_data);
                }
            })
        });
    }

    const updateInventoryName = event => {
        setInventoryName(event.target.value);
    }

    const updateInventoryAmount = event => {
        setInventoryAmount(event.target.value);
    }

    useEffect(() => {
        if (tab === 1) {
            setName("Inventories");
            fetchData(`${inventoryURL}?page=1&items=2`);
        } else {
            setName("Deleted Inventories")
            fetchData(`${delInventoryURL}?page=1&items=2`);
        }
    }, [tab])

    const handleAdd = () => {
        const url = `${process.env.REACT_APP_API_DOMAIN}/inventory`;
        const amountValue = Number.parseInt(inventoryAmount);
        if (amountValue === null) {
            alert("Amount must be integer");
            return;
        }
        const body = {
            name: inventoryName,
            amount: amountValue
        }
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }).then(response => {
            return response.json();
        }).then(data => {
            alert(data.message);
            if (data.status_code === 200) {
                window.location.reload();
            }
        })
    }

    return (
        <Box
            style={{
                width: "100vw",
                height: "100vh",
                display: "flex",
                alignItems: "center",
                flexDirection: "column"
            }}
        >
            <Box
                style={{
                    width: "50vw",
                }}
            >
                <Tabs
                    value={tab}
                    onChange={changeTab}
                    aria-label="wrapped label tabs example"
                >
                    <Tab value={1} label="Inventories" />
                    <Tab value={2} label="Deleted" />
                </Tabs>
            </Box>
            <Box>
                <Typography style={{
                    fontSize: "40px"
                }}>
                    {name}
                </Typography>
            </Box>
            {tab === 1 &&
                <Button
                    variant="contained"
                    onClick={() => setAddModal(true)}
                >
                    Add
                </Button>
            }
            <ListInventory inventories={inventories} setPage={setTab}/>
            <PaginationInventory
                paging={paging}
                url={tab === 1 ? inventoryURL : delInventoryURL}
                fetchData={fetchData}
            />

            <Modal
                open={addModal}
                onClose={() => setAddModal(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Add New Inventory
                    </Typography>
                    <Box
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            width: "100%",
                            height: "100%",
                            justifyContent: "space-evenly"
                        }}
                    >
                        <TextField
                            id="inventory_name"
                            label="Name"
                            variant="outlined"
                            onChange={updateInventoryName}
                        />
                        <TextField
                            id="inventory_amount"
                            label="Amount"
                            variant="outlined"
                            onChange={updateInventoryAmount}
                        />
                        <Button variant="contained" onClick={handleAdd}>Submit</Button>
                    </Box>
                </Box>
            </Modal>
        </Box>
  );
}

export default MainPage;