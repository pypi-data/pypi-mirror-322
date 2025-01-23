import streamlit as st

from utils import Http, Log


class Admin:
    @classmethod
    def load_list(cls, path, params):
        records = Http.send_request_json_response(
            path, "GET", params=params, debug=True
        )
        if not records:
            st.error(f"Failed to get records with {params=}")
            return None

        st.success(f"Received {len(records)} records from the server.")
        for record in records:
            Log.ui_debug(record)
        return records

    @classmethod
    def load_record(cls, path, params):
        records = cls.load_list(path, params)
        return records[0] if records else None

    @classmethod
    def submit_record(cls, path, id_value, json):
        method = "POST"
        if id_value > 0:
            method = "PUT"
            json["id"] = id_value

        record = Http.send_request_json_response(path, method, json=json, debug=True)
        if not record:
            return

        st.success("Success")
        st.json(record, expanded=True)

    @classmethod
    def delete_record(cls, path, params):
        record = Http.send_request_json_response(
            path, "DELETE", params=params, debug=True
        )
        if not record:
            # Backend would send 200 OK even if id not found.
            st.error(f"Failed to delete a record with {params=}")
            return

        st.success("Success")
        st.json(record, expanded=True)
