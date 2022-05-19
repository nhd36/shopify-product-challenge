import {Box, Stack} from "@mui/material";
import Inventory from "./Inventory";

const ListInventory = ({ inventories, setPage}) => {
    const imageDomain = `${process.env.REACT_APP_API_DOMAIN}/inventory/image`
    return (
        inventories !== null &&
            <Stack
                spacing={3}
                width="60%"
                style={{
                    marginBottom: "2em"
                }}
            >
                {inventories.map((data, index) => {
                    const image = `${imageDomain}/${data.id}`;
                    return (<Inventory
                        data={data}
                        image={image}
                        setPage={setPage}
                        key={index}
                    />)
                })}
            </Stack>
    )
}

export default ListInventory;