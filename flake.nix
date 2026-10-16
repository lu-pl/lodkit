{
  description = "LODKit development shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    swls.url = "github:SemanticWebLanguageServer/swls";
  };

  outputs = { nixpkgs, flake-utils, swls, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            ## package definitions go here
            python312
            uv
            ruff
            # swls.packages.${system}.default
          ];
        };
      }
    );
}
