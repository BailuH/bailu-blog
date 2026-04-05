/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { PydanticObjectId } from './PydanticObjectId';
import type { RolesEnum } from './RolesEnum';

export type UserDocument = {
    /**
     * MongoDB document ObjectID
     */
    _id?: (PydanticObjectId | null);
    username: string;
    email: string;
    role?: (RolesEnum | null);
    disabled?: (boolean | null);
    created_at?: (string | null);
    updated_at?: (string | null);
    avatar_url?: (string | null);
};

