package com.github.L_Ender.cataclysm.client.model.entity;

import com.github.L_Ender.cataclysm.client.model.CMModelLayers;
import com.github.L_Ender.cataclysm.client.animation.Labubu_Animation;
import com.github.L_Ender.cataclysm.entity.Pet.Labubu_Entity;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;

public class Labubu_Model extends HierarchicalModel<Labubu_Entity> {
    // This layer location should be baked with EntityRendererProvider.Context in the entity renderer and passed into this model's constructor
    public static final ModelLayerLocation LAYER_LOCATION = CMModelLayers.LABUBU_MODEL;
    private final ModelPart root;
    private final ModelPart body_group;
    private final ModelPart head_group;
    private final ModelPart left_arm_group;
    private final ModelPart right_arm_group;
    private final ModelPart left_leg_group;
    private final ModelPart right_leg_group;

    public Labubu_Model(ModelPart root) {
        this.root = root.getChild("root");
        this.body_group = this.root.getChild("body_group");
        this.head_group = this.body_group.getChild("head_group");
        this.left_arm_group = this.body_group.getChild("left_arm_group");
        this.right_arm_group = this.body_group.getChild("right_arm_group");
        this.left_leg_group = this.body_group.getChild("left_leg_group");
        this.right_leg_group = this.body_group.getChild("right_leg_group");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition meshdefinition = new MeshDefinition();
        PartDefinition partdefinition = meshdefinition.getRoot();

        PartDefinition root = partdefinition.addOrReplaceChild("root", CubeListBuilder.create(), PartPose.offset(0.0F, 24.0F, 0.0F));

        PartDefinition body_group = root.addOrReplaceChild("body_group", CubeListBuilder.create().texOffs(0, 14).addBox(-4.0F, -10.0F, -2.5F, 8.0F, 7.0F, 5.0F, new CubeDeformation(0.0F))
        .texOffs(28, 6).addBox(-3.0F, -9.0F, -3.5F, 6.0F, 3.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition head_group = body_group.addOrReplaceChild("head_group", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -6.0F, -3.5F, 8.0F, 7.0F, 7.0F, new CubeDeformation(0.0F))
        .texOffs(26, 14).addBox(-4.0F, -10.0F, -1.5F, 3.0F, 5.0F, 3.0F, new CubeDeformation(0.0F))
        .texOffs(28, 22).addBox(1.0F, -10.0F, -1.5F, 3.0F, 5.0F, 3.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, -10.0F, 0.0F));

        PartDefinition left_arm_group = body_group.addOrReplaceChild("left_arm_group", CubeListBuilder.create().texOffs(30, 0).addBox(-1.5F, -1.0F, -1.5F, 3.0F, 5.0F, 3.0F, new CubeDeformation(0.0F)), PartPose.offset(-5.5F, -9.0F, 0.0F));

        PartDefinition right_arm_group = body_group.addOrReplaceChild("right_arm_group", CubeListBuilder.create().texOffs(28, 30).addBox(-1.5F, -1.0F, -1.5F, 3.0F, 5.0F, 3.0F, new CubeDeformation(0.0F)), PartPose.offset(5.5F, -9.0F, 0.0F));

        PartDefinition left_leg_group = body_group.addOrReplaceChild("left_leg_group", CubeListBuilder.create().texOffs(0, 26).addBox(-1.5F, -1.0F, -2.0F, 3.0F, 4.0F, 4.0F, new CubeDeformation(0.0F)), PartPose.offset(-2.0F, -3.0F, 0.0F));

        PartDefinition right_leg_group = body_group.addOrReplaceChild("right_leg_group", CubeListBuilder.create().texOffs(14, 26).addBox(-1.5F, -1.0F, -2.0F, 3.0F, 4.0F, 4.0F, new CubeDeformation(0.0F)), PartPose.offset(2.0F, -3.0F, 0.0F));

        return LayerDefinition.create(meshdefinition, 64, 64);
    }

    @Override
    public void setupAnim(Labubu_Entity entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        this.root().getAllParts().forEach(ModelPart::resetPose);
        this.animateHeadLookTarget(netHeadYaw, headPitch);
        this.animate(entity.idleAnimationState, Labubu_Animation.IDLE, ageInTicks, 1.0F);
        this.animateWalk(Labubu_Animation.WALK, limbSwing, limbSwingAmount, 2.0F, 2.0F);
        this.animate(entity.sitAnimationState, Labubu_Animation.SIT, ageInTicks, 1.0F);
    }

    private void animateHeadLookTarget(float yRot, float xRot) {
        this.head_group.xRot = xRot * ((float) Math.PI / 180F);
        this.head_group.yRot = yRot * ((float) Math.PI / 180F);
    }

    @Override
    public ModelPart root() {
        return this.root;
    }

    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer vertexConsumer, int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
        root.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}