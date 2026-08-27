
const apiClient = {
    async get<T>(url: string): Promise<T> {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        return handleResponse<T>(response);
    },

    async post<T, B>(url: string, body: B): Promise<T> {
        const isFormData = body instanceof FormData;

        const response = await fetch(url, {
            method: "POST",
            ...(isFormData
                ? {}
                : {
                    headers: {
                        "Content-Type": "application/json",
                    },
                }),

            body: isFormData
                ? body
                : JSON.stringify(body),
        });

        return handleResponse<T>(response);
    },

    async put<T, B>(url: string, body: B): Promise<T> {
        const response = await fetch(url, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        return handleResponse<T>(response);
    },

    async delete<T>(url: string): Promise<T> {
        const response = await fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        });

        return handleResponse<T>(response);
    },
};

async function handleResponse<T>(
    response: Response
): Promise<T> {
    if (!response.ok) {
        const error = await response.text();

        throw new Error(
            `HTTP ${response.status}: ${error || response.statusText
            }`
        );
    }

    if (response.status === 204) {
        return undefined as T;
    }

    return response.json();
}

export default apiClient;
