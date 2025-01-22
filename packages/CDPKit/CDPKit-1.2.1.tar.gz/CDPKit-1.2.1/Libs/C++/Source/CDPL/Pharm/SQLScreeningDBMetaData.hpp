/* 
 * SQLScreeningDBMetaData.hpp
 *
 * This file is part of the Chemical Data Processing Toolkit
 *
 * Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; see the file COPYING. If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */


#ifndef CDPL_PHARM_SQLSCREENINGDBMETADATA_HPP
#define CDPL_PHARM_SQLSCREENINGDBMETADATA_HPP

#include <string>


namespace CDPL
{

    namespace Pharm
    {

        namespace SQLScreeningDB
        {

            const std::string MOL_TABLE_NAME       = "molecules";
            const std::string PHARM_TABLE_NAME     = "pharmacophores";
            const std::string FTR_COUNT_TABLE_NAME = "ftr_counts";

            const std::string MOL_ID_COLUMN_NAME       = "mol_id";
            const std::string MOL_HASH_COLUMN_NAME     = "mol_hash";
            const std::string MOL_DATA_COLUMN_NAME     = "mol_data";
            const std::string MOL_CONF_IDX_COLUMN_NAME = "mol_conf_idx";

            const std::string PHARM_DATA_COLUMN_NAME = "pharm_data";

            const std::string FTR_TYPE_COLUMN_NAME  = "ftr_type";
            const std::string FTR_COUNT_COLUMN_NAME = "ftr_count";
        } // namespace SQLScreeningDB
    } // namespace Pharm
} // namespace CDPL

#endif // CDPL_PHARM_SQLSCREENINGDBMETADATA_HPP
