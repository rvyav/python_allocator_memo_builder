import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import type { AnalysisData } from "../types/analysis";

interface ResultState { result: AnalysisData | null }

const initialState: ResultState = { result: null };

const resultSlice = createSlice({
    name: "result",
    initialState,
    reducers: {
        setResult: (state, action: PayloadAction<AnalysisData>) => {
            state.result = action.payload;
        },
        clearResult: (state) => {
            state.result = null;
        },
    },
});

export const {
    setResult,
    clearResult,
} = resultSlice.actions;

export default resultSlice.reducer;
