#/bin/bash
set -e

##
# Compile function which will call make function in individual packages
##
function compile() {
    local pkg="${1}"
    local pkg_name=$(echo "${pkg}" | cut -d '/' -f 2)

    cd "${pkg}" || exit 1

    # Generate packages
    make

    # Zip & Copy build artifacts to different location so it can be picked up by circleci
    tar -czf "../../dist-packages/${pkg_name}.tar.gz" -C build/UBUNTU18_64/ .

    cd ../../ || exit 1
}

##
# Main function which gets list of packages which are updated compared to develop branch
# and calls compile function to compile the package
##
function main() {
    local modified_only="${1:-false}"

    # Remove folder if already present
    if [ -d "dist-packages" ]; then
        rm -Rf dist-packages;
    fi

    # Create destination folder
    mkdir dist-packages

    while IFS= read -r pkg
    do
        # @TODO check if package has modifications
        echo -e "################## Compiling \"${pkg}\" ..."
        compile "${pkg}"
    done < "scripts/build-packages"
}

main "$@"

