import {Pagination, Stack} from "@mui/material";

const PaginationInventory = ({paging, fetchData, url}) => {
    const handleChange = (event, value) => {
        fetchData(`${url}?page=${value}&items=2`)
    }
    return (
        <Stack spacing={2}>
            <Pagination
                count={paging.total}
                color="secondary"
                onChange={handleChange}
            />
        </Stack>
    );
}

export default PaginationInventory;