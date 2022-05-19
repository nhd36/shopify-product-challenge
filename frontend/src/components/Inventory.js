import {Box, Button, Modal, TextField, Typography, Input} from "@mui/material";
import {useState} from "react";

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

const Inventory = ({data, image, setPage}) => {
    const date = new Date(data.created_at*1000);
    const hours = `${date.getHours()}`.padStart(2, '0')
    const minutes = `${date.getMinutes()}`.padStart(2, '0');
    const seconds = `${date.getSeconds()}`.padStart(2, '0');
    const dateStr = date.toDateString();

    const [editModal, setEditModal] = useState(false);
    const [imageModal, setImageModal] = useState(false);

    const [editName, setEditName] = useState(null);
    const [editAmount, setEditAmount] = useState(null);

    const handleName = event => {
        setEditName(event.target.value);
    }

    const handleAmount = event => {
        setEditAmount(event.target.value);
    }

    let url = data.deleted_at === null ?
        `${process.env.REACT_APP_API_DOMAIN}/inventory/${data.id}` :
        `${process.env.REACT_APP_API_DOMAIN}/inventory/undelete/${data.id}`;

    const imageUploadURL = `${process.env.REACT_APP_API_DOMAIN}/inventory/image/${data.id}`;

    const fetchData = (url, method, page) => {
        fetch(url, {
                method: method,
            }).then(response => {
                return response.json()
            }).then(response => {
                if (response.status_code === 200) {
                    setPage(page)
                    alert(response.message)
                }
            })
    }
    const handleDelete = () => {
        if (data.deleted_at) {
            fetchData(url, "PUT", 1);
        } else {
            fetchData(url, "DELETE", 2);
        }
    }

    const handleEdit = () => {
        const amountInt = Number.parseInt(editAmount);
        if (amountInt === null) {
            alert("Amount must be integer");
            return;
        }
        const data = {
            name: editName,
            amount: amountInt
        }
        fetch(`${url}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(response => {
            return response.json();
        }).then(data => {
            alert(data.message);
            if (data.status_code === 200) {
                window.location.reload();
            }
        })
    }

    const handleUploadImage = (event) => {
        const formData = new FormData();
        formData.append("image", event.target.files[0]);
        console.log(imageUploadURL);
        fetch(imageUploadURL, {
            method: "PUT",
            body: formData,
            headers: {
                "Accept": "application/json",
                "type": "formData"
            }
        }).then(response => {
            return response.json()
        }).then(data => {
            alert(data.message);
            window.location.reload();
        })
    }

    return (
        <Box
            boxShadow={20}
            style={{
                borderRadius: "25px",
                width: "100%",
                height: "200px",
                padding: "20px",
                display: "flex",
                justifyContent: "space-around",
                alignItems: "center",
            }}
        >
            <Box>
                <Typography>
                    <b>ID:</b> {data.id}
                </Typography>
                <Typography>
                    <b>Name:</b> {data.name}
                </Typography>
                <Typography>
                    <b>Amount:</b> {data.amount}
                </Typography>
                <Typography>
                    <b>Created At:</b> <i>{dateStr} at {hours}:{minutes}:{seconds}</i>
                </Typography>

            </Box>
            <Box
                style={{
                    width: "20%",
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "space-evenly"
                }}
            >
                {!data.deleted_at && <Button
                    variant="contained"
                    color="warning"
                    onClick={() => setEditModal(true)}
                >
                    Edit
                </Button>}
                <Button
                    variant="contained"
                    color={data.deleted_at ? "primary" : "error" }
                    onClick={handleDelete}
                >
                    {data.deleted_at ? "Restore" : "Delete"}
                </Button>
                {data.has_image && !data.deleted_at &&
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => setImageModal(true)}
                    >
                        View Image
                    </Button>}
                {!data.deleted_at &&
                    <label htmlFor="image_file">
                        <Input
                            style={{
                                display: "none"
                            }}
                            accept="image/*"
                            id="image_file"
                            type="file"
                            onChange={handleUploadImage}
                        />
                        <Button
                            fullWidth
                            variant="contained"
                            color="secondary"
                            component="span"
                        >
                            Upload Image
                        </Button>
                    </label>
                }
            </Box>
            <Modal
                open={editModal}
                onClose={() => setEditModal(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Edit inventory ID: {data.id}
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
                            onChange={handleName}
                        />
                        <TextField
                            id="inventory_amount"
                            label="Amount"
                            variant="outlined"
                            onChange={handleAmount}
                        />
                        <Button variant="contained" onClick={handleEdit}>Submit</Button>
                    </Box>
                </Box>
            </Modal>
            <Modal
                open={imageModal}
                onClose={() => setImageModal(false)}
            >
                <Box
                    style={{
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        transform: 'translate(-50%, -50%)',
                        backgroundColor: 'background.paper',
                        boxShadow: 24,
                    }}
                >
                    <img src={image}/>
                </Box>
            </Modal>
        </Box>
    )
}

export default Inventory;